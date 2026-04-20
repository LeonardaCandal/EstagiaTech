from dataclasses import dataclass

# ── 1. Exceções Personalizadas (Tratamento de Erros) ──
class EstagiaTechErro(Exception): pass
class IdadeMinimaErro(EstagiaTechErro): pass
class CandidaturaDuplicadaErro(EstagiaTechErro): pass

# ── 2. Dataclasses / DTOs (Armazenamento de Dados) ──
@dataclass
class Contato:
    email: str
    telefone: str

@dataclass
class Endereco:
    cidade: str
    estado: str

# ── 3. Herança 3 Níveis (Estrutura POO) ──
class Pessoa:
    def __init__(self, nome: str, idade: int, contato: Contato):
        self.nome = nome
        self.idade = idade
        self.contato = contato

    def apresentar(self) -> str:
        return f"Pessoa: {self.nome}"

class Estudante(Pessoa):
    def __init__(self, nome: str, idade: int, contato: Contato, curso: str):
        super().__init__(nome, idade, contato)
        self.curso = curso

    def apresentar(self) -> str:
        return f"[Estudante] {self.nome} | Curso: {self.curso}"

class EstudanteTI(Estudante):
    def __init__(self, nome: str, idade: int, contato: Contato, curso: str, github: str):
        super().__init__(nome, idade, contato, curso)
        self.github = github
        self.vagas_candidatadas = []

    def apresentar(self) -> str:
        base = f"{self.nome} | GitHub: {self.github}"
        if self.vagas_candidatadas:
            vagas = ", ".join([v.titulo for v in self.vagas_candidatadas])
            return f"{base} \n      ↳ Concorrendo a: {vagas}"
        return base
    
# ── 4. Herança Múltipla ──
class Empregadora:
    def receber_candidatura(self, nome_candidato: str, titulo_vaga: str) -> str:
        return f"O candidato {nome_candidato} entrou no processo seletivo para {titulo_vaga}!"

class Empresa(Pessoa, Empregadora):
    def __init__(self, nome: str, idade: int, contato: Contato, setor: str, endereco: Endereco):
        Pessoa.__init__(self, nome, idade, contato)
        self.setor = setor
        self.endereco = endereco

    def apresentar(self) -> str:
        return f"{self.nome} | Setor: {self.setor} | Sede: {self.endereco.cidade}"

# ── 5. Classe Vaga ──
class Vaga:
    def __init__(self, titulo: str, empresa: Empresa, qtd: int):
        self.titulo = titulo
        self.empresa = empresa
        self.qtd = qtd

    def apresentar(self) -> str:
        return f"{self.titulo} na {self.empresa.nome} (Total: {self.qtd} vagas)"
    
# ── 6. Listas em Memória ──
estudantes = []
empresas = []
vagas = []

# ── FUNÇÃO DE VISUALIZAÇÃO (Polimorfismo / Duck Typing) ──
def exibir_secao(titulo: str, lista_objetos: list):
    print(f"\n{titulo} ({len(lista_objetos)}):")
    if not lista_objetos:
        print("   ↳ Nenhum registro no momento.")
    else:
        for item in lista_objetos:
            print("   ↳ " + item.apresentar())


# ── 7. Sistema Principal (CLI) ──
def main():
    while True:
        print("\n" + "="*35)
        print("MENU ESTAGIATECH")
        print("="*35)
        print("1. Cadastrar Estudante de TI")
        print("2. Cadastrar Empresa")
        print("3. Criar Vaga")
        print("4. Realizar Candidatura")
        print("5. Dashboard (Visão Geral)")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        try:
            match opcao:
                case "1":
                    nome = input("Nome: ")
                    idade = int(input("Idade: "))
                    if idade < 18: raise IdadeMinimaErro("É necessário ter 18+ para estagiar.")
                    email = input("Email: ")
                    github = input("Usuário do GitHub: ")
                    
                    novo_estudante = EstudanteTI(nome, idade, Contato(email, ""), "Sistemas de Informação", github)
                    estudantes.append(novo_estudante)
                    print("Estudante cadastrado!")
                case "2":
                    nome = input("Nome da Empresa: ")
                    cidade = input("Cidade Sede: ")
                    
                    nova_empresa = Empresa(nome, 10, Contato("", ""), "Tecnologia", Endereco(cidade, "ES"))
                    empresas.append(nova_empresa)
                    print("Empresa cadastrada!")

                case "3":
                    if not empresas: raise EstagiaTechErro("Cadastre uma empresa primeiro!")
                    
                    print("Empresas disponíveis:", [e.nome for e in empresas])
                    nome_emp = input("Digite o nome da empresa ofertante: ")
                    
                    busca_emp = [e for e in empresas if e.nome.lower() == nome_emp.lower()]
                    if not busca_emp: raise EstagiaTechErro("Empresa não encontrada.")

                    titulo = input("Título da vaga (ex: Dev Python): ")
                    qtd = int(input("Quantidade total de vagas: "))
                    vagas.append(Vaga(titulo, busca_emp[0], qtd))
                    print("Vaga criada!")
                case "4":
                    if not estudantes or not vagas: 
                        raise EstagiaTechErro("Cadastre pelo menos um estudante e uma vaga primeiro.")
                    
                    print("Estudantes disponíveis:", [e.nome for e in estudantes])
                    nome_est = input("Digite o nome do estudante que vai se candidatar: ")
                    
                    busca_est = [e for e in estudantes if e.nome.lower() == nome_est.lower()]
                    if not busca_est: raise EstagiaTechErro("Estudante não encontrado.")
                    
                    estudante_atual = busca_est[0] 

                    print("\nVagas Disponíveis:")
                    for v in vagas:
                        print(f"- {v.titulo} na {v.empresa.nome}")
                        
                    titulo_vaga = input(f"\nPara qual vaga {estudante_atual.nome} deseja se candidatar? ")
                    
                    busca_vaga = [v for v in vagas if v.titulo.lower() == titulo_vaga.lower()]
                    if not busca_vaga: raise EstagiaTechErro("Vaga não encontrada.")

                    vaga_alvo = busca_vaga[0]

                    if vaga_alvo in estudante_atual.vagas_candidatadas:
                        raise CandidaturaDuplicadaErro("O estudante já se candidatou a esta vaga!")

                    estudante_atual.vagas_candidatadas.append(vaga_alvo)
                    print(f"\n{vaga_alvo.empresa.receber_candidatura(estudante_atual.nome, vaga_alvo.titulo)}")
                    
        except ValueError:
            print("Erro: Digite um número inteiro onde for exigido (Idade ou Quantidade).")
        except EstagiaTechErro as e:
            print(f"Regra de Negócio: {e}")
        else:
            if opcao not in ("0", "_"):
                print("✔ Operação realizada com sucesso.")
        finally:
            print("-" * 35)

if __name__ == "__main__":
    main()
