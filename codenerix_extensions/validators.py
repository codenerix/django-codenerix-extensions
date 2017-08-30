import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def spanishNIFNIECIFhelper(cid):
    '''
    Given a spanish NIF, CIF or NIE, it returns:

    1 for a valid NIF
    2 for a valid CIF
    3 for a valid NIE
    -1 for an invalid NIF (it looks like NIF but it doesn't validate the CRC)
    -2 for an invalid CIF (it looks like CIF but it doesn't validate the CRC)
    -3 for an invalid NIE (it looks like NIE but id doesn't validate the CRC)
    -4 not a valid NIF/NIE/CIF because it is too long
    -5 not a valid NIF/NIE/CIF because it doesn't have a valid format
    -6 it can not recognize if it is NIF, CIF or NIE, conclusion: the given CID is incorrect.
    '''

    # Set upper case
    cid = cid.upper()

    # Already too long?
    if len(cid) > 9:
        # Incorrect CID
        return -4

    # Check the format
    compiled = re.compile('((^[A-Z]{1}[0-9]{7}[A-Z0-9]{1}$|^[T]{1}[A-Z0-9]{8}$)|^[0-9]{8}[A-Z]{1}$)')
    if not compiled.match(cid):
        # It doesn't have a valid format, incorrect CID
        return -5

    # Build a string with digits for NIF checks
    num = ''
    for i in range(0, len(cid)):
        num += cid[i]

    # Standar NIF checks
    compiled = re.compile('(^[0-9]{8}[A-Z]{1}$)')
    if compiled.match(cid):
        # It looks like NIF
        index = int(cid[0:8]) % 23
        string = 'TRWAGMYFPDXBNJZSQVHLCKE'
        if (num[8] == string[index]):
            # Valid NIF
            return 1
        else:
            # Invalid NIF
            return -1

    # Build a string for CIF checks
    suma = int(num[2]) + int(num[4]) + int(num[6])
    for i in range(1, len(num), 2):
        codigo = str(2 * int(num[i]))
        a = int(codigo[0])
        if len(codigo) == 2:
            b = int(codigo[1])
        else:
            b = 0
        suma += (a+b)
    n = 10 - int(str(suma)[-1])

    # Special NIFs (they are checked as CIFs)
    compiled = re.compile('^[KLM]{1}')
    if compiled.match(cid):
        # It looks like a Special NIF
        if num[8] == chr(64 + n):
            # Valid NIF
            return 1
        else:
            # Invalid NIF
            return -1

    # Standar CIF checks
    compiled = re.compile('^[ABCDEFGHJNPQRSUVW]{1}')
    if compiled.match(cid):
        # It looks like CIF
        if (num[8] == chr(64 + n)) or (num[8] == str(n)[-1]):
            # Valid CIF
            return 2
        else:
            # Invalid CIF
            return -2

    # Standard NIE checks, T kind
    compiled = re.compile('^[T]{1}')
    if compiled.match(cid):
        # It looks like NIE
        if num[8] == len(re.split('^[T]{1}[A-Z0-9]{8}$', cid)[0]):
            # Valid NIE
            return 3
        else:
            # Invalid NIE
            return -3

    # Standard NIE checks, XYZ kind
    compiled = re.compile('^[XYZ]{1}')
    if compiled.match(cid):
        # It looks like NIE
        string = 'TRWAGMYFPDXBNJZSQVHLCKE'
        cid = cid.replace('X', '0')
        cid = cid.replace('Y', '1')
        cid = cid.replace('Z', '2')
        if num[8] == string[int(cid[0:8]) % 23]:
            # Valid NIE
            return 3
        else:
            # Invaid NIE
            return -3

    # Default fall out is unrecogniced CID, so it is incorrect
    return -6


def spanishNIFNIECIF(nif=True, nie=True, cif=True, details=True):

    def worker(cid, nif, nie, cif, details):
        # Make analisys
        kind = spanishNIFNIECIFhelper(cid)

        # Prepare basic answers
        if kind < 0:
            if details:
                if nif and kind == -1:
                    raise ValidationError(_('NIF %(cid)s is misspelled'), params={'cid': cid})
                elif cif and kind == -2:
                    raise ValidationError(_('CIF %(cid)s is misspelled'), params={'cid': cid})
                elif nie and kind == -3:
                    raise ValidationError(_('NIE %(cid)s is misspelled'), params={'cid': cid})
                elif kind == -4:
                    raise ValidationError(_('CID %(cid)s is too long'), params={'cid': cid})
                elif kind == -5:
                    raise ValidationError(_('CID %(cid)s has a wrong format'), params={'cid': cid})
                elif kind == -6:
                    raise ValidationError(_('CID %(cid)s is incorrect'), params={'cid': cid})

            # In any other case, it is incorrect
            raise ValidationError(_('%(cid)s is incorrect'), params={'cid': cid})

        # Check for valid CIDs which are not allowed
        elif kind == 1 and not nif:
            if details:
                raise ValidationError(_('NIFs are not allowed in this field'))
            else:
                raise ValidationError(_('CID %(cid)s is incorrect'), params={'cid': cid})
        elif kind == 2 and not cif:
            if details:
                raise ValidationError(_('CIFs are not allowed in this field'))
            else:
                raise ValidationError(_('CID %(cid)s is incorrect'), params={'cid': cid})
        elif kind == 3 and not nie:
            if details:
                raise ValidationError(_('NIEs are not allowed in this field'))
            else:
                raise ValidationError(_('CID %(cid)s is incorrect'), params={'cid': cid})

    # Return function
    return lambda cid: worker(cid, nif, nie, cif, details)


# Alias as necesary for migrate to work
def spanishNIFNIE(cid):
    func = spanishNIFNIECIF(cif=False)
    func(cid)


if __name__ == "__main__":

    nifs = []
    nifs.append(('12345678Z', '12344678Z'))
    cifs = []
    cifs.append(('A58818501', 'A58813501'))
    cifs.append(('Q3638496D', 'Q3638496C'))
    nies = []
    nies.append(('Z3698658X', 'Z3698458X'))
    invalids = []
    invalids.append(('1234567890Z', -4, 'INCORRECT'))
    invalids.append(('A12X4567Z', -5, 'INCORRECT'))
    invalids.append(('O12345678', -6, 'INCORRECT'))

    idx = 1
    tests = []
    for (ts, r, k) in [(nifs, 1, 'NIF'), (cifs, 2, 'CIF'), (nies, 3, 'NIE')]:
        for (v, i) in ts:
            tests.append((v, r, k))
            tests.append((i, -r, k))
    for (t, r, k) in invalids:
        tests.append((t, r, k))

    for (value, result, kind) in tests:
        res = spanishNIFNIECIFhelper(value)
        assert res == result, "TestA {}: {} {} detection if failing, expected {} and got {}".format(idx, kind, value, result, res)
        print("Test A/{}: {} {} passed)".format(idx, kind, value))
        idx += 1

    idx = 1
    func = spanishNIFNIECIF()
    for (value, result, kind) in tests:
        try:
            func(value)
            valid = True
        except ValidationError as e:
            valid = False

        assert (valid == bool(result > 0)), "TestB {}: {} {} validation is failing, expected {} and got {}".format(idx, kind, value, bool(result > 0), valid)
        print("Test B/{}: {} {} passed)".format(idx, kind, value))
        idx += 1

    idx = 1
    for (value, result, kind) in tests:
        try:
            spanishNIFNIE(value)
            valid = True
        except ValidationError as e:
            valid = False

        assert (valid == bool((result > 0) and (kind != 'CIF'))), "TestC {}: {} {} validation is failing, expected {} and got {}".format(idx, kind, value, bool((result > 0) and (kind != 'CIF')), valid)
        print("Test C/{}: {} {} passed)".format(idx, kind, value))
        idx += 1
