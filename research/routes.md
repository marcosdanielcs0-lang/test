# Investigação de rotas: ZZZ Steam e Fortnite

Resultados em 21/10/2026; referências, estado de acesso e hashes das páginas lidas em `route-sources.json`. Nenhum loader foi instalado ou jogo iniciado. Fontes upstream são móveis; estes hashes identificam o texto consultado, não verificam binários. Não foram copiados pacotes ou código de terceiros ao projeto.

## XXMI / ZZMI

O README oficial do XXMI lista ZZMI como model importer, instalação automatizada pelo próprio launcher e licença GPLv3. Isso não significa que Melty o instala nem autorização do editor do ZZZ. O código oficial `zzmi_package.py` usa `InjectMode.HOOK`, configura renderização e tem referências a `GameLaunch.STEAM`. Também contém configuração opcional que escreve `GENERAL_DATA.bin`. Nenhuma dessas operações foi executada. Uma condição nesse código consulta configuração WWMI; sua presença não permite assegurar funcionamento da variante Steam.

O README encontrado no branch master de ZZMI-Package descreve **WWMI/Wuthering Waves**, não ZZZ. A URL main retornou 404. Não reutilizar essas instruções para instalar no ZZZ. A inconsistência impede usar esse README como confirmação de versões suportadas.

3Dmigoto é documentado como wrapper DX11 e ferramenta de modding de renderização. Modelos, texturas, shaders, hotkeys ou variáveis de renderização não demonstram criação de missões, dano autoritativo, entidades de gameplay, persistência de loot. Não foi encontrada API documentada desses sistemas nas fontes examinadas. Isso não afirma que seja impossível escrever outro software; apenas que ZZMI não oferece a capacidade exigida demonstrada.

Não foi confirmada permissão do editor, compatibilidade anticheat ou execução da versão Steam instalada. Não desabilitar proteções para experimentar. O original MIT não torna XXMI GPLv3 redistribuível sob MIT; qualquer distribuição teria de cumprir sua licença e as regras Melty, além de resolver os bloqueios técnicos.

## Outras extensões ZZZ

BepInEx documenta plugins Unity Mono/IL2CPP. MelonLoader documenta sua infraestrutura de plugins/mods. São frameworks genéricos: não comprovam acesso autorizado aos sistemas do ZZZ nem compatibilidade Steam. Unity como engine não torna jogos intercambiáveis. Não foram instalados nem escolhidos como adaptadores. Nenhum SDK oficial de extensões de gameplay ZZZ foi identificado nas fontes acessíveis; ausência de evidência não é prova de inexistência universal.

`game_info(custom-zenless-zone-zero)` foi consultado novamente: permite primary/custom folder, mas não oferece loader ou configuração de versão. Isso não é aprovação de XXMI, ZZMI, BepInEx ou MelonLoader. Sem binário real, receita e instalação testada, não executar one_click_check com um pacote vazio para obter uma aprovação enganosa. Suporte a um clique continua **não verificado**, e não declarado impossível apenas por faltar um loader no catálogo.

## Fortnite sem containers criptografados

`game_info(fortnite)` continua excluindo mods do cliente e leitura/substituição de IoStore criptografado. Sugestões genéricas UE4SS no mesmo resultado não autorizam aplicação nesse cliente.

Candidatos para investigação adicional, **sem implementação prometida**:

- **UEFN/Verse e Analytics:** possível ambiente oficial para conteúdo/eventos em ilhas Fortnite, mas a documentação Epic foi bloqueada por HTTP 403 do proxy. Não foi validada uma saída de eventos para um processo externo, sua latência, permissão, autenticação ou receita Melty. Mesmo um evento legítimo precisaria de receptor real no ZZZ; trocar o host para uma ilha viola a escolha atual.
- **Fortnite Data API:** documentação bloqueada pelo mesmo proxy. Não está demonstrado que forneça eventos individuais ao vivo ou conteúdo da cópia instalada. Métricas agregadas, caso disponíveis, não equivalem a eventos do jogador e não comprovam um mashup dependente de sua instalação.
- **Overwolf Game Events Provider:** documentação específica também bloqueada; tentativa de documentação-fonte GitHub não recuperou uma página válida. Não foram confirmados eventos suportados, condições de uso, runtime distribuível ou execução em um clique. Uma ponte externa baseada em provedor autorizado seria candidata a eventos reais, mas não se pode inventar sua API nem declarar segurança sem documentação e teste.
- **Logs/replays locais:** nenhum contrato documentado de exportação ao vivo foi identificado nas fontes lidas. Não presumir conteúdo, formato ou estabilidade; nunca obter tokens de contas, ler memória protegida ou substituir proteção por captura improvisada. Não implementado.

## Bloqueio e próximo marco

Não há rota demonstrada que reúna **ZZZ Steam + permissão + missões individuais/combate PvE/loot + instalação Melty em um clique**, nem fonte Fortnite real validada sob as restrições. Windows é necessário para confirmar versões e comportamento de qualquer rota permitida; não resolve sozinho ausência de API ou permissão. A documentação Epic/Overwolf precisa ficar acessível para avaliar esses candidatos, independentemente do Windows.

As planilhas `design/routes.json` e `design/systems.json` preservam as incógnitas, e o preflight rejeita rota visual como host de gameplay, ausência de confirmação Steam, permissão, teste de instalação e evidência de runtime. Todos os resultados são pesquisa; não constituem build jogável ou aprovação do Melty.


## Reavaliação single-player

O escopo vigente tem exatamente um jogador e não exige cooperação, sincronização de rede, servidores próprios nem testes com dois clientes. Resultados brutos de outros mashups mantêm metadados históricos; não são requisitos.

`game_info` foi consultado novamente para ZZZ e Fortnite após a mudança de escopo. ZZZ continua sem loader/configuração específica, e Fortnite continua sem rota permitida para modificar seu cliente ou ler containers criptografados. ZZMI documenta renderização, não hooks de objetivo, conclusão PvE e concessão de loot. Não há, nas fontes lidas, uma rota permitida e comprovada para implementar sequer a missão mínima individual no ZZZ Steam. A mudança reduz requisitos, mas não transforma plugins visuais em API de missão.

A especificação em `design/missions.json` exige um encontro PvE real, contribuição Fortnite com proveniência e recompensa única. Hooks e recompensa estão nulos por falta de API validada; não foram implementados adaptadores especulativos ou testes que aleguem gameplay. Para desbloquear: demonstrar no Windows uma extensão permitida do ZZZ capaz de aceitar objetivo, observar o encontro real e conceder loot, além da contribuição real Fortnite. Nenhum desses requisitos pede servidor próprio ou sincronização entre jogadores.
