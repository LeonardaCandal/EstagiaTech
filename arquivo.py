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