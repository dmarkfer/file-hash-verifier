import sys

import requests
import json

import hashlib
import base64
import binascii


class FileHashVerifier:

    urlGetMethodHeaders = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


    def retrieveRootHashes(self, urlGetRootHashes: str):
        getRequestRootHashes = requests.get(urlGetRootHashes, headers = FileHashVerifier.urlGetMethodHeaders)

        if(getRequestRootHashes.status_code != 200):
            raise Exception('GET method has failed while fetching root hashes.')
        
        self.jsonArrayRootHashes = json.loads(getRequestRootHashes.text)
        self.nFiles = len(self.jsonArrayRootHashes)
    

    class FileData:

        def __init__(self, rootHash: str, nPieces: int):
            self.rootHash = rootHash
            self.nPieces = nPieces
        

        class PieceData:

            def __init__(self, rootHash: str, pieceOrdinalNumber: int):
                self.rootHash = rootHash
                self.pieceOrdinalNumber = pieceOrdinalNumber
        

            def retrieveAndVerify(self, urlGetPieceData: str):
                getRequestPieceData = requests.get(
                    urlGetPieceData + '/' + self.rootHash + '/' + str(self.pieceOrdinalNumber),
                    headers = FileHashVerifier.urlGetMethodHeaders
                )

                if getRequestPieceData.status_code != 200:
                    raise Exception('GET method has failed while fetching piece data.')
        
                self.jsonPieceData = json.loads(getRequestPieceData.text)

                content = str(self.jsonPieceData['content'])
                proof = self.jsonPieceData['proof']

                contentRaw = base64.decodebytes(content.encode('ascii'))
                constructedHash = hashlib.sha256(contentRaw).hexdigest()

                nProofs = len(proof)

                for treeLevel in range(nProofs):
                    elementOfProof = str(proof[treeLevel])

                    if self.pieceOrdinalNumber >> treeLevel & 1:
                        concatAggregate = elementOfProof + constructedHash
                    else:
                        concatAggregate = constructedHash + elementOfProof
            
                    constructedHash = hashlib.sha256(binascii.unhexlify(concatAggregate)).hexdigest()
            
                self.valid = True if constructedHash == self.rootHash else False
            
                return self.valid
