import git;
import os;
import pathlib;
from slugify import slugify;
from .terminal import Terminal;

class GitOp:
	def __init__(self):
		self.git = GitOp.status('.');

	def init(self):
		if (self.exists() == False):
			Terminal.err('Comando Inválido', 'O repositório já foi iniciado na pasta atual...');

		pname = slugify(Terminal.askInput('[*] Qual o nome do projeto?', 25));

		if ( pathlib.Path(pathlib.PurePath('.', 'README.md')).is_file() != True ) :
			os.system('echo "# {name}" >> README.md'.format(name = pname));

		self.git = git.Repo.init('.').git;
		self.__commit(':tada: initial(repo): First commit');
		self.__renameTo('main');

		add_origin = Terminal.askInput('[*] Adicionar origem remota?');
		origin_name = None;
		origin_url = None;

		if (add_origin):
			origin_name = Terminal.askInput('[*] Informe o nome da origem:', default = 'origin');
			origin_url = Terminal.askInput('[*] Qual a URL de origem do projeto?');

			self.__remote(origin_url, origin_name);
			self.__pushTo('main');

		self.__create('dev', origin_name, add_origin);
		Terminal.success('Repositório inicializado com sucesso...');

	def commit (self):
		branch = self.__currentBranch();
		Terminal.shouldContinue();

		type = Terminal.commitTypes();
		print();

		scope = Terminal.askInput('[*] Dê um escopo para o seu commit [<=15]', 15);
		title = Terminal.askInput('[*] Dê um título para o seu commit [<=50]', 50);
		body = Terminal.askInput('Descreva brevemente o seu commit [<=75]', 75, False, '');

		message = "{em} {tp}({sc}): {tt}\n\n{b}".format(em=type['emoji'],tp=type['type'],sc=scope,tt=title,b=body);

		Terminal.printSuccess('Pré-visualização do commit:\n');
		print(message+"\n");

		Terminal.shouldContinue();

		self.__commit(message);

		_continue = Terminal.askInput('Deseja exportar o commit para branches remotos [push]?');

		if ( _continue != False ):
			self.__pushTo(branch);
			Terminal.success('Commit finalizado e sincronizado com sucesso...');

		Terminal.success('Commit finalizado com sucesso...');

	def exists (self):
		return self.git != False;

	def __remote(self, url: str, name: str = 'origin'):
		self.git.remote('add', name, url);

	def __create(self, branch: str, origin: str = 'origin', track: bool = True):
		if ( track ):
			self.git.checkout('-b', branch, '--track', origin+'/'+branch);
		else:
			self.git.checkout('-b', branch);

	def __pushTo(self, branch: str, origin: str = 'origin', upstream: bool = True):
		if ( upstream ):
			self.git.push('-u', origin, branch);
		else:
			self.git.push(origin, branch);

	def __renameTo(self, new: str):
		self.git.branch('-M', new);

	def __commit(self, message: str):
		self.git.add('--all');
		self.git.commit('-m', message);

	def __currentBranch(self):
		print("Você está atualmente no branch:");
		branch = self.git.branch('--show-current');
		Terminal.printSuccess(branch);
		return branch;

	@staticmethod
	def status (target):
		try:
			return git.Repo(target).git;
		except git.InvalidGitRepositoryError:
			return False;