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