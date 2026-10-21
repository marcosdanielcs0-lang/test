# Viabilidade atual — single-player

O escopo oficial é um jogador, com ZZZ Steam como principal e Fortnite como complementar obrigatório. Missões individuais, combate PvE e loot continuam previstos. Multiplayer, cooperação entre jogadores, sincronização de rede e servidores próprios estão fora do escopo; os jogos comerciais ainda podem exigir seus serviços normais.

A conexão autenticada MCP funciona. Nova consulta `game_info` dos dois jogos após a mudança de escopo não revelou uma rota nova: Melty aceita ZZZ como primary, sem fornecer loader ou versão específicos. Isso não demonstra suporte a extensões de gameplay. Fortnite permanece sem loader suportado e com containers IoStore criptografados, que não serão lidos ou substituídos.

XXMI/ZZMI e 3Dmigoto documentam renderização/modelos, não missão, eventos PvE ou loot no ZZZ Steam. BepInEx/MelonLoader são frameworks genéricos; não comprovam compatibilidade nem permissão para esse jogo. A análise e as fontes estão em `routes.md` e `route-sources.json`.

Os exemplos LockerCraft/Locker Drop e Zenless R.E.P.O. foram consultados como pesquisa. As receitas disponíveis não demonstram um leitor Fortnite reutilizável ou execução de gameplay dentro do ZZZ. Registros JSON antigos mantêm fatos de outros projetos, incluindo multiplayer; não definem requisitos para este projeto.

**Bloqueio preciso:** falta uma rota permitida e testada no ZZZ Steam que ofereça objetivo de missão, evento PvE e concessão de loot; falta também fonte real de conteúdo/eventos Fortnite sob as restrições. Remover multiplayer não elimina esses dois bloqueios. Não foi produzida versão jogável, instalador especulativo ou demonstração substituta. `build_ready: false`; publicação bloqueada.

## Próxima validação no Windows

1. Verificar instalações e versões com `tools/Inspect-LocalGames.ps1` (somente presença/FileVersion, ainda não executado).
2. Identificar e comprovar uma rota de extensão permitida no ZZZ Steam, sem alterar arquivos protegidos ou contornar proteções. Não instalar loaders sem autorização.
3. Demonstrar a contribuição real Fortnite, sem modificar seu cliente ou ler containers criptografados. Documentação Epic/Overwolf continua sem validação por bloqueio de rede na consulta anterior.
4. Somente então implementar a missão mínima de `design/missions.json`, testar aceitação, evento PvE, loot e prevenção de recompensa duplicada dentro do ZZZ com um jogador.
5. Registrar evidência da versão executada, validar instalação Melty e capturar gameplay real antes de considerar publicação. Não iniciar jogos sem autorização.

Acesso ao Windows por si só não resolve ausência de APIs/permissão. Testes Python exercitam ferramentas e critérios, nunca gameplay.
