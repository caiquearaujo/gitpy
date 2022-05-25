#!/usr/bin/env python
import colorama;
import git;
import os;
import pathlib;
import sys;

def status (target):
	try:
		return git.Repo(target).git;
	except git.InvalidGitRepositoryError:
		return False;

def devBranch (repo: git.Git):
	repo.checkout('-b', 'dev');
	repo.push('-u', 'origin', 'dev');

def repoInit(target): 
	sts = status(target);

	if ( sts != False ):
		err('Comando Inválido', 'O repositório já foi iniciado na pasta atual...');

	project_name = queryInput('Qual o nome do projeto? > ');
	has_origin = queryYN('Tem uma origem remota? > ');

	if (has_origin):
		repo_origin = queryInput('Qual a URL de origem do projeto? > ');

	if ( pathlib.Path(pathlib.PurePath(target, 'README.md')).is_file() != True ) :
		os.system('echo "# {name}" >> README.md'.format(name = project_name));
	
	repo = git.Repo.init(target).git;
	repo.add('--all');
	repo.commit('-m', ':tada: initial(repo): First commit');
	repo.branch('-M', 'main');

	if (has_origin):
		repo.remote('add', 'origin', repo_origin);
		repo.push('-u', 'origin', 'main');

	sys.stdout.write("\n\nRepositório iniciado com sucesso...")

def repoCommit(_git):
	print("Você está realizando um commit no branch:");
	print(colorama.Fore.GREEN + _git.branch('--show-current') + colorama.Fore.RESET);
	_continue = queryYN('Deseja prosseguir?');

	if ( _continue == False ):
		success();

	commit_types = {
		1: { 'emoji': ':sparkles:', 'type': 'feat', 'txt': "Features" },
		2: { 'emoji': ':bug:', 'type': 'fix', 'txt': "Bug Fixes" },
		3: { 'emoji': ':books:', 'type': 'docs', 'txt': "Documentation" },
		4: { 'emoji': ':gem:', 'type': 'style', 'txt': "Styles" },
		5: { 'emoji': ':package:', 'type': 'refactor', 'txt': "Code Refactoring" },
		6: { 'emoji': ':racehorse:', 'type': 'perf', 'txt': "Performance Improvements" },
		7: { 'emoji': ':rotating_light:', 'type': 'test', 'txt': "Tests" },
		8: { 'emoji': ':wrench:', 'type': 'build', 'txt': "Builds" },
		9: { 'emoji': ':gear:', 'type': 'ci', 'txt': "Continuous Integrations" },
		10: { 'emoji': ':recycle:', 'type': 'chore', 'txt': "Chores" },
		11: { 'emoji': ':rewind:', 'type': 'revert', 'txt': "Reverts" },
		12: { 'emoji': ':arrow_double_up:', 'type': 'dependencies', 'txt': "Dependencies" },
		13: { 'emoji': ':arrow_double_up:', 'type': 'peerDependencies', 'txt': "Peer dependencies" },
		14: { 'emoji': ':arrow_double_up:', 'type': 'devDependencies', 'txt': "Dev dependencies" },
		15: { 'emoji': ':card_index:', 'type': 'metadata', 'txt': "Metadata" },
		16: { 'emoji': ':bookmark:', 'type': 'version', 'txt': "Version tag" },
		17: { 'emoji': ':lock:', 'type': 'security', 'txt': "Security" },
		18: { 'emoji': ':pencil:', 'type': 'text', 'txt': "Text" },
		19: { 'emoji': ':ambulance:', 'type': 'critical', 'txt': "Critical changes" },
		20: { 'emoji': ':ok_hand:', 'type': 'review', 'txt': "Code review" },
		21: { 'emoji': '', 'type': 'abort', 'txt': "Abortar commit" },
	};

	type = 0;

	print();

	while (type <= 0):
		for key in commit_types.keys():
			print(key, '\t', commit_types[key]['txt']);

		try:
			print();
			type = int(input('Defina o tipo de commit' + colorama.Fore.GREEN + ' > ' + colorama.Fore.RESET));
		except:
			type = 0;

	if ( type == 21 ): 
		success('Commit abortado com sucesso');
	
	type = commit_types[type];

	print();
	scope = queryInput('Dê um escopo para o seu commit [<=15]', 15);
	title = queryInput('Dê um título para o seu commit [<=50]', 50);
	body = queryInput('Descreva brevemente o seu commit [<=75]', 75);

	message = "{em} {tp}({sc}): {tt}\n\n{b}".format(em=type['emoji'],tp=type['type'],sc=scope,tt=title,b=body);

	_git.add('--all');
	_git.commit('-m', message);

	success('Commit finalizado com sucesso...');

def main () : 
	command = None;

	argv = sys.argv[1:];

	if (len(argv) == 0):
		err('Argumento Inválido', 'Defina um comando antes de continuar...');

	command = argv[0];
	switcher = {
		'dev': lambda _git: devBranch(_git),
		'commit': lambda _git: repoCommit(_git),
	}

	if ( command == 'init' ):
		repoInit('.');
		success();

	func = switcher.get(command, False);

	if ( func == False ):
		err('Comando Inválido', 'O comando {command} não foi encontrado.'.format(command=command));

	_git = status('.');

	if (_git == False):
		err('Comando Inválido', 'O repositório ainda não foi iniciado, execute o comando init antes de continuar.');

	func(_git);
	success();

def queryInput (question: str, max: int = -1):
	while True:
		print(question + colorama.Fore.GREEN + ' > ' + colorama.Fore.RESET);
		response = input();

		if ( max < 0 ):
			max = len(response);

		if (len(response) != 0 and len(response) <= max):
			return response;
		else:
			printErr('Valor inesperado', 'É necessário preencher uma resposta...');

			if (max >= 0):
				printErr('Valor inesperado', 'Limite máximo de {m} caracter(es) atingido...\n'.format(m=max));

def queryYN (question: str, default: str = 'yes'):
	valid = {"yes": True, "y": True, "no": False, "n": False};

	if default is None:
		prompt = " [y/n] ";
	elif default == "yes":
		prompt = " [Y/n] ";
	elif default == "no":
		prompt = " [y/N] ";
	else:
		default = 'yes';
		prompt = " [Y/n] ";

	while True:
		choice = input(question + prompt + colorama.Fore.GREEN + '> ' + colorama.Fore.RESET).lower();

		if default is not None and choice == "":
			return valid[default];
		elif choice in valid:
			return valid[choice];
		else:
			printErr('Valor inesperado', 'Por favor, responda com: `y`, `n`, `yes` ou `no`.');

def printErr (err = 'Erro', message = 'Algo deu errado'):
	print(
		colorama.Back.RED 
		+ err + ' >' 
		+ colorama.Back.RESET 
		+ colorama.Fore.RED 
		+ ' ' + message
		+ colorama.Fore.RESET
	);

def err (err = 'Erro', message = 'Algo deu errado'):
	printErr(err, message);
	sys.exit(2);

def success (message = 'Não há mais nada a ser feito...'):
	print("\n\n" + colorama.Fore.GREEN + message + colorama.Fore.RESET);
	sys.exit();

if __name__ == "__main__":
	main()