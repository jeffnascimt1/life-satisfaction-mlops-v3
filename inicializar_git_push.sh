#!/bin/bash

echo "🚀 Inicializando repositório Git com fluxo dev/main..."

# 1. Verifica se já é um repositório Git
if [ -d .git ]; then
    echo "✅ Este diretório já é um repositório Git."
else
    git init
    echo "✅ Repositório Git inicializado."
fi

# 2. Configura usuário (se necessário)
git config user.name "Jefferson Silva"
git config user.email "jeffnascimt@gmail.com"

# 3. Cria o commit inicial
touch README.md
echo "# Projeto Life Satisfaction MLOps v3" > README.md
git add .
git commit -m "commit inicial"

# 4. Renomeia branch principal para main (se necessário)
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    git branch -M main
    echo "🔄 Branch renomeada para 'main'."
fi

# 5. Adiciona repositório remoto via SSH
git remote remove origin 2>/dev/null
git remote add origin git@github.com:jeffnascimt1/life-satisfaction-mlops-v3.git
echo "🔗 Origin definido para SSH: git@github.com:jeffnascimt1/life-satisfaction-mlops-v3.git"

# 6. Envia para o GitHub
git push -u origin main
echo "✅ Push realizado com sucesso na branch main."

# 7. Cria branch de desenvolvimento
git checkout -b dev
git push -u origin dev
echo "🌱 Branch dev criada e enviada."

echo "🎉 Projeto Git configurado com sucesso!"
