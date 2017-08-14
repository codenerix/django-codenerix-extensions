/*
 *
 * django-codenerix-extensions
 *
 * Copyright 2017 Centrologic Computational Logistic Center S.L.
 *
 * Project URL : http://www.codenerix.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * This library is intended for encrypting as CODENERIX Cryptography's Libraries work, the basis
 * for the library to work are, the KEY is always a SHA256 from your real KEY, the IV vector
 * should be generated automatically on encryption time by the library and must be inserted
 * at the beginning of the encrypted string (which shoul be padded with PKCS7). The full
 * string IV+ENCRYPTED is encoded to Base64. For decrypting the process is the opossite, the
 * raw string is decoded from Base64, the first 16 bytes are taken as the IV and the rest as
 * the encrypted string, the key is hashed with SHA256 and then the encrypted string is decrypted
 * using the IV and the hashed key.
 *
 * This library is working thanks to crypto-js from Jakub Zapletal ( https://github.com/jakubzapletal )
 *
 * You must include the next crypto-js files to let cryptography work as excepcted:
 * <script type="text/javascript" src="/static/codenerix_extensions/lib/crypto-js/core.js"></script>  
 * <script type="text/javascript" src="/static/codenerix_extensions/lib/crypto-js/sha256.js"></script>  
 * <script type="text/javascript" src="/static/codenerix_extensions/lib/crypto-js/enc-base64.js"></script>  
 * <script type="text/javascript" src="/static/codenerix_extensions/lib/crypto-js/cipher-core.js"></script>  
 * <script type="text/javascript" src="/static/codenerix_extensions/lib/crypto-js/aes.js"></script>  
 *
 *  // Some examples
 *  var raw = "1234567890123456";
 *  var key = "1234567890123456";
 *  var raw2 = "eFu34cdc2j30avHkYRIIfoH0JpD2VgkuMIkULxKxvuqwEPt26h33KHzqmnEIPbaX";
 *  var key2 = "123456789012345b";
 *  var raw3 = "hOxLY8VLpi989zsRJZycBZgij2iPM/jYkdq51m3yFy+n/gMGL5Z5YjxcUhitJ81tEcKnz55cTenBaTG0uUcZfqhjQne42LaVWykItm1J/aA=";
 *  var key3 = "La magia ocurre cuando sale el sol";
 *  var raw4 = "When the moon comes to the sky, your eyes shine!";
 *  var key4 = "No matter what you do, the sierpinski cube is beautifull!"
 *
 *  var enc = encrypt(raw, key, "1234567890123456"); console.log(typeof(enc), enc); // Giving an specific IV vector
 *  var dec = encrypt(raw, key);   console.log(typeof(dec), dec);                   // Using automatic IV vector generator
 *  var dec = decrypt(raw2, key2); console.log(typeof(dec), dec);                   // Decrypting
 *  var dec = decrypt(raw3, key3); console.log(typeof(dec), dec);                   // Decrypting
 *  var enc = encrypt(raw4, key4); console.log(typeof(enc), enc);                   // Encrypting
 */

function encrypt(raw, key, iv) {
    // Create the hash from the key
    var hashkey = CryptoJS.SHA256(key);

    // The initialization vector (must be 16 bytes)
    if (typeof(iv) == "undefined") {
        var iv = CryptoJS.lib.WordArray.random(16);
    } else {
        console.warn("You are using an external IV, this is not the way the library is inteded to work, BE CAREFULL this is only for debugging purpose!");
        var iv  = CryptoJS.enc.Utf8.parse(iv);
    }

    // Encrypt
    var enc = CryptoJS.AES.encrypt(raw, hashkey, { iv: iv });

    // Put the result together with the IV
    var mix = iv.concat(enc.ciphertext);

    // Convert to Base 64
    var b64enc = mix.toString(CryptoJS.enc.Base64)

    // We are done
    return b64enc;
}

function decrypt(data, key) {
    // Create the hash from the key
    var hashkey = CryptoJS.SHA256(key);

    // Convert to Base 64
    var full = CryptoJS.enc.Base64.parse(data);

    // Put the result together with the IV
    var iv = CryptoJS.enc.Hex.parse(full.toString(CryptoJS.enc.Hex).slice(0,16*2));
    var raw = CryptoJS.enc.Hex.parse(full.toString(CryptoJS.enc.Hex).slice(16*2));

    // Encrypt
    var todec = CryptoJS.lib.CipherParams.create({ciphertext: raw});
    var dec = CryptoJS.AES.decrypt(todec, hashkey, { iv: iv });
    
    // Get the string
    var str = dec.toString(CryptoJS.enc.Utf8);

    // We are done
    return str;
}
