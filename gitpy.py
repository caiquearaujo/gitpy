#!/usr/bin/env python3
import getopt;
import git;
import os;
import pathlib;
import sys;

def status (target):
	try:
		return git.Repo(target);
	except git.InvalidGitRepositoryError:
		return False;

def repoInit(target): 
	project_name = queryInput('Qual o nome do projeto?');
	has_origin = queryYN('Tem uma origem remota?');

	if (has_origin):
		repo_origin = queryInput('Qual a URL de origem do projeto?');

	# if ( pathlib.Path(pathlib.PurePath(target, 'README.md')).is_file() != True ) :
	# 	os.system('echo "# {name}" >> README.md'.format(name = project_name));
	
	repo = git.Repo.init(target).git;
	repo.add('--all');
	repo.commit('-m', ':tada: initial(repo): First commit');
	repo.branch('-M', 'main');

	if (has_origin):
		repo.remote('add', 'origin', repo_origin);
		repo.push('-u', 'origin', 'main');

	print("Repositório iniciado com sucesso...")

def main () : 
	repo_base = None;
	command = None;

	argv = sys.argv[1:];

	try:
		opts, args = getopt.getopt(argv, "c:p:", ["command=", "path="]);
	except getopt.GetoptError:
		print('Não é possível validar os parâmetros do comando...');
		sys.exit(2);

	for opt, arg in opts:
		if ( opt in ( '-c', '--command' ) ):
			command = arg;
		elif ( opt in ( '-p', '--path' ) ):
			repo_base = arg;

	if command is None:
		command = 'init';

	if repo_base is None:
		repo_base = '.';

	repo_base = str(pathlib.Path(repo_base).resolve());

	if ( status(repo_base) == False ):
		repoInit(repo_base);

def queryInput (question: str):
	while True:
		sys.stdout.write(question);
		response = input();

		if len(response) != 0:
			return response;
		else:
			sys.stdout.write("Por favor, insira uma resposta válida.\n")

def queryYN (question: str, default: str = 'yes'):
	valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False};

	if default is None:
		prompt = " [y/n] ";
	elif default == "yes":
		prompt = " [Y/n] ";
	elif default == "no":
		prompt = " [y/N] ";
	else:
		raise ValueError("Invalid default answer: '%s'" % default);

	while True:
		sys.stdout.write(question + prompt);
		choice = input().lower();

		if default is not None and choice == "":
			return valid[default];
		elif choice in valid:
			return valid[choice];
		else:
			sys.stdout.write("Por favor, responda com: y; n; yes; no.\n")

if __name__ == "__main__":
	main()