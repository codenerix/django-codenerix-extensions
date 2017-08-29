import re


def spanishNIFNIECIF(cid):
    '''
    Given a spanish NIF, CIF or NIE, it returns:

    1 for a valid NIF
    2 for a valid CIF
    3 for a valid NIE
    -1 for an invalid NIF (it looks like NIF but it doesn't validate the CRC)
    -2 for an invalid CIF (it looks like CIF but it doesn't validate the CRC)
    -3 for an invalid NIE (it looks like NIE but id doesn't validate the CRC)
    0 it can not recognize if it is NIF, CIF or NIE, conclusion: the given CID is incorrect.
    '''

    # Set upper case
    cid = cid.upper()

    # Already too long?
    if len(cid) > 9:
        # Incorrect CID
        return 0

    # Check the format
    compiled = re.compile('((^[A-Z]{1}[0-9]{7}[A-Z0-9]{1}$|^[T]{1}[A-Z0-9]{8}$)|^[0-9]{8}[A-Z]{1}$)')
    if not compiled.match(cid):
        # It doesn't have a valid format, incorrect CID
        return 0

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
    compiled=re.compile('^[KLM]{1}')
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
    return 0


if __name__ == "__main__":
    print(spanishNIFNIECIF('12345678Z'))
