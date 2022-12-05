import unittest

from FileHashVerifier import *


class TestHashTree(unittest.TestCase):

    urlGetRootHashes = 'http://localhost:8080/hashes'
    urlGetPieceData = 'http://localhost:8080/piece'


    def test(self):
        verifier = FileHashVerifier()
        verifier.retrieveRootHashes(TestHashTree.urlGetRootHashes)

        for fileOrdinalNumber in range(verifier.nFiles):
            fileData = FileHashVerifier.FileData(
                str(verifier.jsonArrayRootHashes[fileOrdinalNumber]['hash']),
                int(verifier.jsonArrayRootHashes[fileOrdinalNumber]['pieces'])
            )

            for pieceOrdinalNumber in range(fileData.nPieces):
                pieceData = FileHashVerifier.FileData.PieceData(fileData.rootHash, pieceOrdinalNumber)
                result = pieceData.retrieveAndVerify(TestHashTree.urlGetPieceData)

                with self.subTest(msg='File=' + str(fileOrdinalNumber) + ', Piece=' + str(pieceOrdinalNumber)):
                    self.assertEqual(result, True)

unittest.main()
