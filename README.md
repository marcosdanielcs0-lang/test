# Fortnite × New Eridu

Crossover **single-player**: missões individuais, combate PvE, loot e integração real entre Zenless Zone Zero e Fortnite. **Ainda não existe versão jogável ou integração testada. `build_ready: false`.**

## Escopo oficial

- Principal obrigatório: Zenless Zone Zero (Unity), versão Steam.
- Complementar obrigatório: Fortnite (Unreal Engine), fornecendo conteúdo ou eventos reais por rota permitida.
- Um jogador. Sem multiplayer, cooperação entre jogadores, sincronização de rede ou servidores próprios. Isso não promete que os jogos comerciais funcionem offline.
- Código original MIT; remixes permitidos. A licença não abrange conteúdo, marcas ou software dos jogos.
- Usar cópias instaladas do jogador, sem distribuir arquivos proprietários, ler containers criptografados, modificar o cliente Fortnite ou contornar proteções.
- Não substituir por jogo independente ou demo de navegador. Não instalar loaders nem iniciar jogos sem autorização.

## Primeiro marco mínimo

Uma missão individual dentro do ZZZ usa uma contribuição real do Fortnite, acompanha um encontro PvE real e concede loot uma única vez por conclusão. `design/missions.json` descreve esse alvo, não uma implementação: hooks, recompensa e contribuição permanecem pendentes até haver APIs comprovadas. Não são inventados IDs de inimigos, APIs, tabelas de drops ou resultados de gameplay.

## Fontes de verdade e aceitação

- `design/systems.json`: host, companion, missões, combate PvE e loot. Nenhum sistema de cooperação.
- `design/routes.json`: capacidades, permissão, compatibilidade Steam e instalação Melty das rotas candidatas.
- `design/missions.json`: especificação mínima e referências; células pendentes bloqueiam o build.
- `design/acceptance.json`: critérios obrigatórios de aceitação single-player. Não existem requisitos de dois clientes ou servidores.
- `research/routes.md`, `research/route-sources.json`: fontes e limites da pesquisa.
- `research/feasibility.md`: conclusão técnica atual. Resultados JSON de pesquisas anteriores são registros históricos; suas receitas e estatísticas não definem o escopo deste projeto.

A aceitação exige execução no ZZZ real, contribuição Fortnite com proveniência, missão/PvE/loot observados no jogo, instalação permitida e evidência da versão testada. Testes Python não satisfazem esses critérios. O preflight não aceita um mod visual como API de gameplay. Declarar flags de sucesso não substitui implementação ou revisão.

## Instalações Windows informadas

- ZZZ: `E:\SteamLibrary\steamapps\common\Zenless Zone Zero`
- Executável relativo: `games\ZenlessZoneZero Game\ZenlessZoneZero.exe`
- Fortnite: `E:\jogos\Fortnite`

Não acessíveis nesta nuvem Linux. `tools/Inspect-LocalGames.ps1` verifica apenas presença/versão dos executáveis; não inicia jogos nem valida gameplay.

## Desenvolvimento na nuvem

Python 3.12+, sem dependências externas. Execute da raiz do repositório:

- `python3 -m unittest discover -s tests -v`: testes de ferramentas, contratos, planilhas e empacotamento.
- `python3 tools/preflight.py`: retorna 1 enquanto houver pendências; saída atual esperada `build_ready: false`.
- `python3 -m tools.package`: pacote reproduzível de fontes MIT e especificações não verificadas em `dist/Fortnite-New-Eridu-development.zip`, com manifesto e checksums. Não é instalador ou build jogável.
- `python3 -m tools.package --release`: recusa a geração de release enquanto os adaptadores e a validação real estiverem ausentes.

`new_eridu/contracts.py` contém somente interfaces para futuros adaptadores. O gerador preserva cada célula das linhas de sistemas, inclusive valores pendentes, sem gerar gameplay ou evidência. O pacote exclui credenciais, anexos de conversa e arquivos proprietários.

## Bloqueio atual

Melty aceita ZZZ como primary, mas não fornece loader/configuração específica. XXMI/ZZMI documentam renderização; não demonstram hooks permitidos de missão, PvE ou loot no ZZZ Steam. Frameworks genéricos Unity não comprovam essa compatibilidade. O Fortnite permanece sem fonte real validada sob as restrições.

A remoção do multiplayer não resolve esses dois bloqueios. Nenhum loader foi instalado ou jogo iniciado. O próximo passo requer identificar uma rota de extensão permitida e demonstrá-la no Windows com os jogos instalados. Publicação no Melty permanece bloqueada; uma futura publicação também depende de instalação validada e mídia real de gameplay.
