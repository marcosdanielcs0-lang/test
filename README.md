# Fortnite × New Eridu

Projeto de crossover cooperativo com missões, combate e loot. **Em definição técnica; ainda não existe uma versão jogável ou publicada verificada.**

## Decisões do criador

- Host obrigatório: Zenless Zone Zero (Unity).
- Companion obrigatório: Fortnite (Unreal Engine).
- Código original: MIT; remixes permitidos. Isso não licencia conteúdo ou marcas dos jogos.
- Usar as cópias instaladas pelo jogador; não distribuir arquivos dos jogos.
- Não substituir o projeto por um jogo independente ou demo de navegador.

## Instalações informadas no Windows

- ZZZ: `E:\SteamLibrary\steamapps\common\Zenless Zone Zero`
- Executável relativo: `games\ZenlessZoneZero Game\ZenlessZoneZero.exe`
- Fortnite: `E:\jogos\Fortnite`

Esses caminhos foram fornecidos pelo criador, mas não puderam ser inspecionados nesta máquina Linux. Não iniciar jogos no PC sem autorização.

## Estado e bloqueios

O checkout estava vazio, sem commits. Nenhum código ou build anterior foi encontrado.

O briefing fornecido informa que o Melty não instala loader para Fortnite, não modifica seu cliente e encontrou seus containers criptografados. Não foi estabelecida uma forma compatível de trazer conteúdo ou gameplay real dele ao ZZZ. Não extrair conteúdo criptografado nem contornar anti-cheat.

Também falta confirmar uma rota de modding para ZZZ, as versões dos jogos, o transporte cooperativo e o limite de jogadores. Não há servidor, sincronização, hospedagem ou ingresso implementados.

Após atualização e republicação, a conexão autenticada MCP do Melty funcionou. As consultas e a análise estão em `research/feasibility.md`; os resultados estruturados foram preservados em `research/*.json`. O download do modding kit ainda foi bloqueado no redirecionamento.

## Próxima etapa

As consultas `game_info`, `search_mashups` e dois exemplos `mashup_info` foram realizadas. Falta confirmar uma integração suportada com evidências locais antes de gerar código de gameplay. Se a integração real não for possível, obter acordo do criador antes de mudar o conceito.

As planilhas em `design/systems.json` registram os sistemas previstos e o que ainda exige evidência. Células pendentes bloqueiam o build; esta documentação não constitui implementação.

Publicação requer build instalado e testado, teste cooperativo com dois clientes, receita validada e imagem real de gameplay. Nenhuma dessas etapas foi concluída. Não há pacote para download.

## Ferramentas preparadas

- `python3 tools/preflight.py`: verifica células pendentes, referências e requisitos; retorna 1 enquanto o build estiver bloqueado.
- `python3 -m unittest discover -s tests -v`: testa as rejeições do preflight.
- No Windows, `powershell -File tools/Inspect-LocalGames.ps1`: inspeção somente de leitura; não executada nesta nuvem.

MIT e remixes permitidos continuam sendo os requisitos do código original. Nenhum conteúdo de terceiros foi incorporado. Não há autorização para publicar.

## Desenvolvimento na nuvem

Python 3.12 ou superior, sem dependências externas. Não há interface web nem gameplay independente.

- `python3 -m unittest discover -s tests -v`: valida ferramentas, contratos e empacotamento; não testa jogos.
- `python3 tools/preflight.py`: saída 1 esperada enquanto houver pendências. Evidências declaradas não habilitam o runtime: a implementação e verificação dos adaptadores continuam ausentes.
- `python3 -m tools.package`: gera `dist/Fortnite-New-Eridu-development.zip`, somente fontes MIT e especificações não verificadas, com manifesto e SHA-256 por arquivo. Usa lista explícita de arquivos: não inclui anexo original, credenciais, arquivos dos jogos ou executáveis.
- `python3 -m tools.package --release`: recusa a criação de release. O desbloqueio exigirá implementação e revisão específicas; não basta preencher as células.

`new_eridu/contracts.py` define interfaces e identidade/versionamento para futuros adaptadores. Não injeta código, não lê memória, não abre containers e não conecta jogadores. `tools/generate_contracts.py` transforma cada linha da planilha em uma especificação imutável serializada durante o empacotamento, preservando inclusive os valores pendentes. Isso não é um build de gameplay e não substitui o preflight obrigatório antes de um futuro build.

O pacote inicial não é instalável pelo Melty e não constitui receita validada. Não publicar. Antes de haver gameplay, ainda é necessário comprovar uma rota permitida entre os dois jogos, implementar os adaptadores reais, definir o transporte cooperativo e testar as mecânicas em instalações locais. Não foram escolhidos danos, tabelas de loot, capacidade de sessão ou APIs dos jogos sem evidência.
