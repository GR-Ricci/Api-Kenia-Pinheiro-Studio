# Entrega para CI/CD — Vercel + Neon

## O que foi adicionado

- `main.py`: entrypoint da Vercel e adaptador de compatibilidade. Não altera arquivos em `app/`.
- `vercel.json`: configura a função Python da Vercel.
- `.env.example`: variáveis que devem ser cadastradas na Vercel.
- `.github/workflows/ci.yml`: valida sintaxe e importação; não inventa testes.
- `requirements.txt`: convertido para UTF-8 e complementado com `PyJWT` e `python-multipart`.

## Deploy automático

Conecte este repositório à Vercel e configure `main` como Production Branch. A Vercel fará Preview para pull requests e Production Deployment após merge em `main`.

No GitHub, proteja `main` em **Settings → Branches**:

- exigir pull request antes do merge;
- exigir o status `Validate deploy package`;
- bloquear push direto para usuários comuns.

O workflow não publica por conta própria. A publicação é feita pela integração Git da Vercel depois que o merge permitido em `main` ocorrer.

## Variáveis na Vercel

Configure em **Settings → Environment Variables**:

- `DATABASE_URL`: string pooled do Neon, com `sslmode=require`;
- `JWT_SECRET_KEY`: segredo forte e exclusivo de produção;
- `CORS_ORIGINS`: deixada preparada, mas a API atual não a lê.

## Limitações preservadas por solicitação

Nenhum arquivo dentro de `app/` foi alterado. Por isso, o CORS da API continua aceitando apenas as origens existentes no código. Se o frontend estiver em outro domínio, ele precisará usar proxy same-origin ou o CORS terá de ser corrigido futuramente na própria API.

A pasta `upload/` continua sendo armazenamento efêmero. Arquivos de produção precisam ser migrados para object storage.
