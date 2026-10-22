import os
import tempfile
import unittest

import main


class ValidacaoTest(unittest.TestCase):
    def test_peca_dentro_das_regras_e_aprovada(self):
        self.assertEqual(main.validar_peca(100, 'Azul', 15), [])

    def test_limites_sao_inclusivos(self):
        self.assertEqual(main.validar_peca(95, 'verde', 10), [])
        self.assertEqual(main.validar_peca(105, 'verde', 20), [])

    def test_lista_todos_os_motivos_de_reprovacao(self):
        erros = main.validar_peca(90, 'vermelho', 25)
        self.assertEqual(len(erros), 3)

    def test_montar_peca_define_status_e_motivo(self):
        peca = main.montar_peca('P1', 110, 'Azul', 15)
        self.assertEqual(peca['status'], 'Reprovada')
        self.assertIn('Peso', peca['motivo'])
        self.assertEqual(peca['cor'], 'azul')


class BancoTest(unittest.TestCase):
    def setUp(self):
        fd, self.caminho = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        self.db_original = main.DB_PATH
        main.DB_PATH = self.caminho
        main.iniciar_db()

    def tearDown(self):
        main.DB_PATH = self.db_original
        os.remove(self.caminho)

    def test_id_duplicado_nao_derruba_o_programa(self):
        self.assertTrue(main.salvar_peca(main.montar_peca('P1', 100, 'azul', 15)))
        self.assertFalse(main.salvar_peca(main.montar_peca('P1', 100, 'azul', 15)))

    def test_excluir_informa_se_encontrou(self):
        main.salvar_peca(main.montar_peca('P1', 100, 'azul', 15))
        self.assertTrue(main.excluir_peca('P1'))
        self.assertFalse(main.excluir_peca('P1'))

    def test_indicadores_e_caixas(self):
        for i in range(12):
            main.salvar_peca(main.montar_peca(f'A{i}', 100, 'verde', 15))
        main.salvar_peca(main.montar_peca('R1', 200, 'verde', 15))

        ind = main.calcular_indicadores()
        self.assertEqual(ind['aprovadas'], 12)
        self.assertEqual(ind['reprovadas'], 1)
        self.assertEqual(ind['caixas_fechadas'], 1)
        self.assertEqual(ind['pecas_na_caixa_atual'], 2)
        self.assertAlmostEqual(ind['taxa_aprovacao'], 12 / 13 * 100)


if __name__ == '__main__':
    unittest.main()
