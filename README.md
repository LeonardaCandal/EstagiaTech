# EstagiaTech — Sistema de Gestão de Estágios em TI

> Avaliação Processual 2026/1 — Modelos e Linguagens de Programação II  
> Faculdade Multivix | Curso: Sistemas de Informação | Período: 4º/5º | Turma: Noturna  
> Professor: Edgard da Cunha Pontes

---

## Integrantes do Grupo

- Jordana Wantil Tomazeli
- Leonarda Candal de Carvalho
- Ronald Cussati Cesar da Fonseca

---

## Descrição do Tema

O **EstagiaTech** é um sistema de console (CLI) para gerenciamento de estágios na área de Tecnologia da Informação. Ele conecta **estudantes de TI** a **empresas** que ofertam **vagas de estágio**, permitindo cadastros e candidaturas de forma simples e interativa pelo terminal.

O sistema gerencia três conceitos principais relacionados entre si:
- **EstudanteTI** — o candidato ao estágio
- **Empresa** — a organização que oferta vagas
- **Vaga** — a oportunidade de estágio vinculada a uma empresa

---

## Como Executar

Certifique-se de ter o **Python 3.10 ou superior** instalado (necessário para o `match/case`).

```bash
python main.py
```

Após iniciar, o menu interativo será exibido no terminal. Navegue digitando o número da opção desejada.

---

## Estrutura e Documentação do Código

### 1. Importação

```python
from dataclasses import dataclass
```

O módulo `dataclasses` é importado para permitir o uso do decorador `@dataclass`, que automatiza a criação de classes de armazenamento de dados (geração automática de `__init__` e `__repr__`).

---

### 2. Exceções Personalizadas

```python
class EstagiaTechErro(Exception): pass
class IdadeMinimaErro(EstagiaTechErro): pass
class CandidaturaDuplicadaErro(EstagiaTechErro): pass
```

**O que são:** Classes que herdam de `Exception`, criadas para representar erros específicos das regras de negócio do sistema.

**Por que existem:** Em vez de usar mensagens genéricas, cada violação de regra tem seu próprio tipo de erro, tornando o tratamento mais preciso e semântico.

| Exceção | Quando é lançada |
|---|---|
| `EstagiaTechErro` | Erro genérico do sistema (base para as demais) |
| `IdadeMinimaErro` | Quando o estudante tem menos de 18 anos |
| `CandidaturaDuplicadaErro` | Quando o estudante tenta se candidatar a uma vaga que já está concorrendo |

**Analogia com C#:** equivale a criar classes que herdam de `Exception` no C#, como `public class IdadeMinimaException : Exception {}`.

---

### 3. Dataclasses — DTOs de Dados

```python
@dataclass
class Contato:
    email: str
    telefone: str

@dataclass
class Endereco:
    cidade: str
    estado: str
```

**O que são:** Classes decoradas com `@dataclass` que funcionam como contêineres de dados simples (DTOs — Data Transfer Objects). Elas **não possuem lógica de negócio**, apenas armazenam informações.

**O que o `@dataclass` faz automaticamente:**
- Gera o método `__init__` com todos os atributos como parâmetros
- Gera o método `__repr__` para exibição legível do objeto

**Type Hints (`email: str`, `cidade: str`):** Indicam o tipo esperado de cada atributo, funcionando como a tipagem estática do C#, mas sem bloquear a execução em caso de tipo errado.

**`Contato`** armazena email e telefone de qualquer entidade do sistema.  
**`Endereco`** armazena cidade e estado da sede de uma empresa.

---

### 4. Herança de 3 Níveis — Hierarquia Principal

```text
Pessoa  →  Estudante  →  EstudanteTI
```

#### Nível 1 — `Pessoa` (classe base)

```python
class Pessoa:
    def __init__(self, nome: str, idade: int, contato: Contato):
        self.nome = nome
        self.idade = idade
        self.contato = contato

    def apresentar(self) -> str:
        return f"Pessoa: {self.nome}"
```

Classe raiz da hierarquia. Define os atributos mais fundamentais que qualquer entidade do sistema pode ter: nome, idade e contato. O método `apresentar()` retorna uma descrição básica — ele será **sobrescrito** nas classes filhas (polimorfismo).

#### Nível 2 — `Estudante` (herda de `Pessoa`)

```python
class Estudante(Pessoa):
    def __init__(self, nome: str, idade: int, contato: Contato, curso: str):
        super().__init__(nome, idade, contato)
        self.curso = curso

    def apresentar(self) -> str:
        return f"[Estudante] {self.nome} | Curso: {self.curso}"
```

Especializa `Pessoa` adicionando o atributo `curso`. O `super().__init__(...)` chama o construtor da classe pai, aproveitando o que já foi definido em `Pessoa` sem reescrever código. O `apresentar()` é sobrescrito para incluir a informação do curso.

**Equivalente em C#:** `public class Estudante : Pessoa { ... }` com `base(nome, idade, contato)` no construtor.

#### Nível 3 — `EstudanteTI` (herda de `Estudante`)

```python
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
```

O nível mais especializado. Além de todos os atributos herdados, adiciona `github` (perfil do estudante) e `vagas_candidatadas` (lista das vagas em que está concorrendo). O `apresentar()` é novamente sobrescrito, agora exibindo também as vagas caso o estudante já tenha se candidatado.

A linha `", ".join([v.titulo for v in self.vagas_candidatadas])` usa uma **List Comprehension** para extrair os títulos de todas as vagas e os une com vírgula numa única string.

---

### 5. Herança Múltipla — `Empresa`

```python
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
```

**`Empregadora`** é uma classe independente que representa a capacidade de receber candidaturas. Ela possui apenas o método `receber_candidatura()`.

**`Empresa(Pessoa, Empregadora)`** herda de **duas classes ao mesmo tempo** (herança múltipla). Isso significa que `Empresa` possui tanto os atributos de `Pessoa` (nome, idade, contato) quanto o comportamento de `Empregadora` (receber candidaturas).

No construtor, `Pessoa.__init__(self, ...)` é chamado explicitamente (em vez de `super()`) porque há múltiplos pais — esta é a forma segura de garantir que o construtor correto seja invocado.

**Analogia com C#:** C# não permite herança múltipla de classes; lá, esse comportamento seria implementado com **interfaces** (`IEmpregadora`). Em Python, a herança múltipla é nativa.

---

### 6. Classe `Vaga`

```python
class Vaga:
    def __init__(self, titulo: str, empresa: Empresa, qtd: int):
        self.titulo = titulo
        self.empresa = empresa
        self.qtd = qtd

    def apresentar(self) -> str:
        return f"{self.titulo} na {self.empresa.nome} (Total: {self.qtd} vagas)"
```

Representa uma oportunidade de estágio. Possui `titulo` (ex: "Dev Python"), uma referência ao objeto `Empresa` que a criou, e `qtd` com o número de vagas disponíveis. O método `apresentar()` é a quarta sobrescrita do mesmo método na hierarquia — contribuindo para o polimorfismo.

---

### 7. Armazenamento em Memória

```python
estudantes = []
empresas = []
vagas = []
```

Três listas globais que funcionam como o "banco de dados" em memória do sistema. Todos os objetos criados durante a execução ficam armazenados aqui. Ao encerrar o programa, os dados são perdidos (sem persistência em arquivo ou banco).

---

### 8. Polimorfismo (Duck Typing) — `exibir_secao()`

```python
def exibir_secao(titulo: str, lista_objetos: list):
    print(f"\n{titulo} ({len(lista_objetos)}):")
    if not lista_objetos:
        print("   ↳ Nenhum registro no momento.")
    else:
        for item in lista_objetos:
            print("   ↳ " + item.apresentar())
```

Esta função demonstra o **polimorfismo por Duck Typing**. Ela recebe qualquer lista de objetos e chama `item.apresentar()` em cada um — sem saber nem se importar se o objeto é um `EstudanteTI`, uma `Empresa` ou uma `Vaga`.

**Por que funciona:** Python não exige que os objetos compartilhem uma interface ou classe base em comum. Basta que todos tenham o método `apresentar()` — se o método existe, ele é chamado. Isso é o Duck Typing: *"se anda como pato e grasna como pato, é um pato"*.

O método `apresentar()` foi sobrescrito em 4 classes (`Estudante`, `EstudanteTI`, `Empresa`, `Vaga`), e cada uma retorna sua própria descrição personalizada.

---

### 9. Menu Principal com `match/case`

```python
match opcao:
    case "1": ...  # Cadastrar Estudante
    case "2": ...  # Cadastrar Empresa
    case "3": ...  # Criar Vaga
    case "4": ...  # Realizar Candidatura
    case "5": ...  # Dashboard
    case "0": ...  # Sair
    case _:  ...   # Opção inválida (equivalente ao default)
```

O `match/case` (disponível a partir do Python 3.10) é a forma moderna de estruturar menus e desvios de fluxo por valor. É equivalente ao `switch/case` do C/C++/C#, porém mais expressivo. O `case _:` funciona como o `default`, capturando qualquer valor não mapeado.

---

### 10. Tratamento de Exceções — `try / except / else / finally`

```python
try:
    # código que pode falhar
except ValueError:
    print("Erro: Digite um número inteiro...")
except EstagiaTechErro as e:
    print(f"Regra de Negócio: {e}")
else:
    if opcao not in ("0", "_"):
        print("✔ Operação realizada com sucesso.")
finally:
    print("-" * 35)
```

| Bloco | Quando executa |
|---|---|
| `try` | Sempre — contém o código principal |
| `except ValueError` | Quando o usuário digita texto onde se espera número (`int()` falha) |
| `except EstagiaTechErro` | Quando uma regra de negócio é violada (inclui subclasses) |
| `else` | **Somente se nenhuma exceção ocorreu** — confirma sucesso da operação |
| `finally` | **Sempre**, independentemente de erro ou sucesso — imprime o separador visual |

**Regras de negócio protegidas:**
1. Estudante deve ter 18 anos ou mais (`IdadeMinimaErro`)
2. Não é possível criar vaga sem empresa cadastrada (`EstagiaTechErro`)
3. O estudante não pode se candidatar duas vezes à mesma vaga (`CandidaturaDuplicadaErro`)

---

### 11. Ponto de Entrada

```python
if __name__ == "__main__":
    main()
```

Garante que a função `main()` só seja executada quando o arquivo for rodado diretamente (`python main.py`), e não quando for importado como módulo por outro arquivo. É uma boa prática padrão em Python, equivalente ao `static void Main()` do C#.

---

## Fluxo Geral do Sistema

```text
Início
  └── Loop do menu (while True)
        ├── Opção 1 → Cadastra EstudanteTI → adiciona em `estudantes[]`
        ├── Opção 2 → Cadastra Empresa     → adiciona em `empresas[]`
        ├── Opção 3 → Cria Vaga            → vincula Empresa → adiciona em `vagas[]`
        ├── Opção 4 → Candidatura          → vincula Estudante + Vaga
        ├── Opção 5 → Dashboard            → exibe todos via exibir_secao()
        └── Opção 0 → Encerra o programa
```

---

## O que achamos mais desafiador na transição para o Python?

A maior diferença percebida foi a **ausência de tipagem estática obrigatória**. Em C/C++/C#, o compilador impede que o código rode se um tipo errado for usado — em Python, os Type Hints são apenas sugestões, e erros de tipo só aparecem em tempo de execução.

Outro ponto desafiador foi o conceito de **`self`**: diferente do `this` em C#, que é implícito, em Python o `self` precisa ser declarado explicitamente como primeiro parâmetro em todo método de instância, o que inicialmente causa estranheza.

Por fim, a **herança múltipla nativa** do Python surpreendeu positivamente: algo que em C# exige o uso de interfaces, em Python pode ser feito diretamente entre classes.

