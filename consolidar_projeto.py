# consolidar_projeto.py
import os
import fnmatch
import sys # Importar sys para verificar a codificação padrão, se necessário, embora utf-8 seja padrão e bom.

def consolidar_projeto():
    # Estrutura específica do seu projeto
    # Assumimos que o script será executado a partir do diretório raiz do projeto "ENCURTADOR-URL"
    project_name = "ENCURTADOR-URL"
    root_directory = "." # O ponto indica o diretório atual (raiz do projeto)

    # Arquivos que queremos incluir (por padrão, tudo que corresponder a estes padrões)
    patterns = [
        '*.py',
        '*.html',
        '*.css',
        '*.js',
        'requirements.txt',
        '*.md',
        '*.txt'
    ]

    # Pastas a ignorar COMPLETAMENTE durante a busca
    ignore_dirs = [
        '__pycache__',
        '.git',
        'venv', # Seu ambiente virtual
        'env', # Outro nome comum para ambiente virtual
        'node_modules', # Se usar frontend com Node.js
        'staticfiles', # Django collectstatic
        '.vscode', # Arquivos de configuração do VS Code
        'migrations', # Ignorar arquivos de migração do Django por padrão
        # Pastas comuns dentro de ambientes virtuais (redundante se 'venv' ou 'env' for ignorado, mas seguro)
        'Include',
        'Lib',
        'Scripts'
    ]

    # Arquivos específicos a ignorar (mesmo que correspondam aos padrões)
    ignore_files = [
        'db.sqlite3', # Banco de dados SQLite
        '*.pyc', # Arquivos Python compilados
        '.gitignore', # Arquivo de configuração do Git
        'pyvenv.cfg' # Arquivo de configuração do ambiente virtual
    ]

    output = []
    output.append("=" * 100)
    output.append("🚀 PROJETO DJANGO: ENCURTADOR DE URL - ANÁLISE COMPLETA")
    output.append("=" * 100)

    # Informações básicas
    output.append(f"\n📋 PROJETO: {project_name}")
    output.append("🎯 TIPO: Django URL Shortener")
    # Usa root_directory para a base do caminho
    output.append("📅 ESTRUTURA CAPTURADA EM: " + os.path.abspath(root_directory))

    # Mapear estrutura
    output.append("\n📁 ESTRUTURA DO PROJETO:")
    output.append("─" * 50)

    # Usar os.walk a partir do diretório raiz especificado
    for root, dirs, files in os.walk(root_directory):
        # Remove pastas ignoradas da busca (modifica a lista dirs in-place)
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Calcula o nível de indentação
        # Se root_directory for '.', o primeiro root será '.', que tem 0 separadores.
        # Se root_directory for uma pasta específica, o primeiro root será essa pasta.
        # A lógica de nível precisa ser ajustada se o root_directory não for '.'
        # Para '.', level é o número de os.sep em root (excluindo o '.')
        # Para uma pasta específica, level é o número de os.sep em root - número de os.sep no root_directory
        # Simplificando para o caso de root_directory = '.'
        if root == '.':
            level = 0
            folder_name = project_name
        else:
            # Calcula o caminho relativo ao root_directory e conta os separadores
            relative_root = os.path.relpath(root, root_directory)
            level = relative_root.count(os.sep) + 1 # +1 porque o próprio subdiretório adiciona um nível
            folder_name = os.path.basename(root)

        indent = '│ ' * level
        output.append(f"{indent}├── 📁 {folder_name}/")

        # Mostrar arquivos relevantes neste diretório
        subindent = '│ ' * (level + 1)
        relevant_files = []
        for file in files:
            # Verifica se o arquivo corresponde a algum padrão E não está na lista de ignorados
            if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                if not any(fnmatch.fnmatch(file, ignore) for ignore in ignore_files):
                    relevant_files.append(file)

        # Ordena os arquivos relevantes para uma saída consistente
        relevant_files.sort()

        for i, file in enumerate(relevant_files):
            connector = "└──" if i == len(relevant_files) - 1 else "├──"
            output.append(f"{subindent}{connector} 📄 {file}")

    output.append("\n" + "=" * 100)
    output.append("📝 CONTEÚDO DOS ARQUIVOS PRINCIPAIS:")
    output.append("=" * 100)

    # Ordem prioritária de arquivos comuns em projetos Django como o seu
    # Ajuste estes caminhos se a estrutura do seu projeto for diferente
    # Ex: 'encurtador/settings.py' assume que 'encurtador' é a pasta de configurações do projeto
    # 'urls/models.py' assume que 'urls' é a pasta do seu app principal
    priority_files = [
        os.path.join(root_directory, 'manage.py'),
        os.path.join(root_directory, 'requirements.txt'),
        os.path.join(root_directory, 'encurtador', 'settings.py'),
        os.path.join(root_directory, 'encurtador', 'urls.py'),
        os.path.join(root_directory, 'urls', 'models.py'),
        os.path.join(root_directory, 'urls', 'views.py'),
        os.path.join(root_directory, 'urls', 'urls.py'),
        os.path.join(root_directory, 'urls', 'admin.py'),
        os.path.join(root_directory, 'urls', 'apps.py')
    ]

    # Primeiro, processar arquivos prioritários
    output.append(f"\n{'🎯 ARQUIVOS PRINCIPAIS (ALTA PRIORIDADE)':=^90}")
    processed_files = set() # Usar um set para rastrear arquivos já processados (usando caminho absoluto)

    for priority_file in priority_files:
        if os.path.exists(priority_file):
            output.extend(process_file(priority_file, root_directory))
            processed_files.add(os.path.abspath(priority_file))

    # Depois, processar templates (procura em uma pasta 'templates' na raiz ou em subpastas de apps)
    # Este loop agora percorre o projeto para encontrar templates
    output.append(f"\n{'🎨 TEMPLATES HTML':=^90}")
    for root, dirs, files in os.walk(root_directory):
         # Remove pastas ignoradas da busca
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith('.html'):
                 file_path = os.path.join(root, file)
                 abs_path = os.path.abspath(file_path)
                 # Processa apenas se não foi processado como arquivo prioritário
                 if abs_path not in processed_files:
                     output.extend(process_file(file_path, root_directory))
                     processed_files.add(abs_path)


    # Processar arquivos estáticos (CSS, JS) - Percorre as pastas static
    output.append(f"\n{'🎨 ARQUIVOS CSS':=^90}")
    output.append(f"\n{'⚙️ ARQUIVOS JAVASCRIPT':=^90}") # Agrupando CSS e JS para simplicidade no loop
    for root, dirs, files in os.walk(root_directory):
         # Remove pastas ignoradas da busca
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Verifica se estamos dentro de uma pasta 'static' ou subpasta dela
        # Uma abordagem mais robusta seria verificar se o caminho contém '/static/'
        is_static_dir = 'static' in root.split(os.sep)

        if is_static_dir:
            for file in files:
                file_path = os.path.join(root, file)
                abs_path = os.path.abspath(file_path)
                # Processa apenas se não foi processado
                if abs_path not in processed_files:
                    if file.endswith('.css') or file.endswith('.js'):
                        output.extend(process_file(file_path, root_directory))
                        processed_files.add(abs_path)


    # Processar arquivos restantes que correspondem aos padrões e não foram processados
    output.append(f"\n{'📄 OUTROS ARQUIVOS RELEVANTES':=^90}")
    for root, dirs, files in os.walk(root_directory):
        # Remove pastas ignoradas da busca
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            abs_path = os.path.abspath(file_path)

            # Verifica se o arquivo não foi processado, corresponde aos padrões e não é ignorado
            if abs_path not in processed_files:
                if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                    if not any(fnmatch.fnmatch(file, ignore) for ignore in ignore_files):
                        output.extend(process_file(file_path, root_directory))
                        processed_files.add(abs_path)

    # Salvar resultado
    output_file = 'projeto_consolidado_encurtador.txt' # Nome de arquivo mais específico
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output))
        print("✅ Projeto consolidado salvo em:", output_file)
        print(f"📊 Total de linhas geradas: {len(output)}")
        print(f"📁 Arquivos processados: {len(processed_files)}")

        # Estatísticas
        file_stats = {}
        for file_path in processed_files:
            # Obtém a extensão do arquivo, incluindo o ponto
            ext = os.path.splitext(file_path)[1]
            # Se não tiver extensão, usa um marcador
            if not ext:
                ext = '[sem extensão]'
            file_stats[ext] = file_stats.get(ext, 0) + 1

        print("\n📈 ESTATÍSTICAS:")
        # Ordena as estatísticas pela extensão
        for ext, count in sorted(file_stats.items()):
            print(f" {ext}: {count} arquivos")

    except IOError as e:
        print(f"❌ Erro ao salvar o arquivo de saída '{output_file}': {e}")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado durante o salvamento: {e}")


def process_file(file_path, root_directory):
    """Processa um arquivo individual, lê o conteúdo e formata a saída."""
    result = []
    # Obtém o caminho relativo ao diretório raiz do projeto
    relative_path = os.path.relpath(file_path, root_directory)

    result.append(f"\n{'─' * 80}")
    result.append(f"🏷️ ARQUIVO: {relative_path}")
    # Obtém o diretório relativo
    relative_dir = os.path.dirname(relative_path)
    result.append(f"📁 LOCALIZAÇÃO: {relative_dir if relative_dir else 'raiz'}")
    result.append(f"{'─' * 80}")

    try:
        # Tenta abrir e ler o arquivo com codificação UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip() # Remove espaços em branco do início/fim

        # Verificar tamanho do conteúdo (pode usar len(content) ou len(content.splitlines()))
        # Usar len(content) para um limite de tamanho em bytes/caracteres
        # Usar len(content.splitlines()) para um limite de linhas
        lines = content.splitlines() # Divide em linhas para contar e limitar
        line_limit = 100 # Limite de linhas para arquivos grandes
        char_limit = 15000 # Limite de caracteres (aprox. 15KB)

        if len(content) > char_limit and len(lines) > line_limit:
             result.append(f"⚠️ ARQUIVO GRANDE ({len(lines)} linhas, ~{len(content)} caracteres) - MOSTRANDO PRIMEIRAS {line_limit} LINHAS")
             result.append('\n'.join(lines[:line_limit]))
             result.append(f"\n... [RESTANTE OMITIDO - {len(lines)-line_limit} linhas restantes]")
        elif len(content) == 0:
            result.append("📝 [ARQUIVO VAZIO]")
        else:
            result.append(content) # Inclui o conteúdo completo se for pequeno

    except UnicodeDecodeError:
        # Captura erro se o arquivo não for UTF-8 (provavelmente binário)
        result.append("⚠️ [ARQUIVO BINÁRIO OU COM CODIFICAÇÃO DIFERENTE - NÃO PODE SER EXIBIDO COMO TEXTO]")
    except FileNotFoundError:
         # Embora os.walk encontre, é uma boa prática ter este catch
         result.append("❌ [ARQUIVO NÃO ENCONTRADO DURANTE O PROCESSAMENTO]")
    except Exception as e:
        # Captura quaisquer outros erros durante a leitura do arquivo
        result.append(f"❌ [ERRO AO LER ARQUIVO: {e}]")

    return result

# Bloco principal para executar a função quando o script for chamado diretamente
if __name__ == "__main__":
    print("🚀 Iniciando consolidação do projeto Django...")
    # O script assume que está sendo executado no diretório raiz do projeto ENCURTADOR-URL
    print("📁 Diretório atual:", os.getcwd())
    # Você pode adicionar uma verificação aqui para garantir que está no diretório correto
    # Ex: verificar se 'manage.py' existe no diretório atual
    if not os.path.exists('manage.py'):
        print("\n⚠️ Parece que você não está executando este script no diretório raiz do seu projeto Django.")
        print("Por favor, navegue até a pasta 'ENCURTADOR-URL' no seu terminal e execute o script novamente.")
        sys.exit(1) # Sai do script com código de erro

    consolidar_projeto()
