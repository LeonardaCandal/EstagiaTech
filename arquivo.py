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