"""Tests unitaires du patron Composite."""

import unittest

from models import Bundle, ProduitNumerique


class TestComposite(unittest.TestCase):
    def setUp(self):
        self.jeu = ProduitNumerique(
            1, "Jeu", "Description", 100.00, 10, "/jeu.jpg"
        )
        self.dlc = ProduitNumerique(
            2, "DLC", "Description", 50.00, 5, "/dlc.jpg"
        )
        self.autre_jeu = ProduitNumerique(
            3, "Autre jeu", "Description", 30.00, 2, "/autre.jpg"
        )

    def test_feuille_prix_et_nombre_items(self):
        self.assertEqual(self.jeu.prix_total(), 100.00)
        self.assertEqual(self.jeu.nb_items(), 1)
        self.assertFalse(self.jeu.est_bundle())

    def test_bundle_calcul_prix_et_items(self):
        bundle = Bundle(
            10, "Bundle", "Description", 0, 1, "/bundle.jpg", rabais=0.20
        )
        bundle.ajouter(self.jeu)
        bundle.ajouter(self.dlc)

        self.assertEqual(bundle.prix_total(), 120.00)
        self.assertEqual(bundle.nb_items(), 2)
        self.assertTrue(bundle.est_bundle())

    def test_imbrication_sur_plusieurs_niveaux(self):
        bundle_interne = Bundle(
            10, "Bundle interne", "Description", 0, 1,
            "/interne.jpg", rabais=0.20
        )
        bundle_interne.ajouter(self.jeu)
        bundle_interne.ajouter(self.dlc)

        bundle_externe = Bundle(
            11, "Bundle externe", "Description", 0, 1,
            "/externe.jpg", rabais=0.10
        )
        bundle_externe.ajouter(bundle_interne)
        bundle_externe.ajouter(self.autre_jeu)

        # (100 + 50) * 0,80 = 120; (120 + 30) * 0,90 = 135.
        self.assertEqual(bundle_externe.prix_total(), 135.00)
        self.assertEqual(bundle_externe.nb_items(), 3)

    def test_feuille_refuse_ajout(self):
        with self.assertRaises(TypeError):
            self.jeu.ajouter(self.dlc)

    def test_bundle_refuse_un_objet_invalide(self):
        bundle = Bundle(10, "Bundle", "Description", 0, 1, "/b.jpg")
        with self.assertRaises(TypeError):
            bundle.ajouter("pas un produit")

    def test_retirer_enfant(self):
        bundle = Bundle(10, "Bundle", "Description", 0, 1, "/b.jpg")
        bundle.ajouter(self.jeu)
        bundle.retirer(self.jeu)
        self.assertEqual(bundle.nb_items(), 0)
        self.assertEqual(bundle.prix_total(), 0.00)


if __name__ == "__main__":
    unittest.main()