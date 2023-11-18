import git;
import os;
import pathlib;
from slugify import slugify;
from .terminal import Terminal;

class GitOp:
	def __init__(self, path):
		self.repo = GitOp.status(path);
		self.path = path;

		if (self.repo != False):
			self.git = self.repo.git;

	def init(self):
		self.repo = git.Repo.init(self.path);
		self.git  = self.repo.git;

	# def commit (self):
	# 	branch = self.currentBranch();
	# 	Terminal.shouldContinue();

	# 	type = Terminal.commitTypes();
	# 	print();

	# 	scope = Terminal.askInput('[*] Dê um escopo para o seu commit [<=15]', 15);
	# 	title = Terminal.askInput('[*] Dê um título para o seu commit [<=50]', 50);
	# 	body = Terminal.askInput('Descreva brevemente o seu commit [<=75]', 75, False);

	# 	message = "{em} {tp}({sc}): {tt}\n\n{b}".format(em=type['emoji'],tp=type['type'],sc=scope,tt=title,b=body);

	# 	Terminal.printSuccess('Pré-visualização do commit:\n');
	# 	print(message+"\n");

	# 	Terminal.shouldContinue();

	# 	self.commit(message);

	# 	_continue = Terminal.askYN('Deseja exportar o commit para branches remotos [push]?');

	# 	if ( _continue != False ):
	# 		self.pushTo(branch);
	# 		Terminal.success('Commit finalizado e sincronizado com sucesso...');

	# 	Terminal.success('Commit finalizado com sucesso...');

	def exists (self):
		return self.git != False;

	def remoteExists (self, name: str):
		if self.git == False:
			return False;

		return name in [remote.name for remote in self.repo.remotes]

	def workingDir (self):
		return self.path;

	def remote(self, url: str, name: str = 'origin'):
		self.git.remote('add', name, url);

	def create(self, branch: str, origin: str = 'origin', track: bool = True):
		if ( track ):
			self.git.checkout('-b', branch);
			self.git.push('-u', origin, branch);
		else:
			self.git.checkout('-b', branch);

	def pushTo(self, branch: str, origin: str = 'origin', upstream: bool = True):
		if ( upstream ):
			self.git.push('-u', origin, branch);
		else:
			self.git.push(origin, branch);

	def renameTo(self, new: str):
		self.git.branch('-M', new);

	def commit(self, message: str):
		self.git.add('--all');
		self.git.commit('-m', message);

	def currentBranch(self):
		branch = self.git.branch('--show-current');
		Terminal.warning("Working branch: " + branch);
		return branch;

	@staticmethod
	def status (target):
		try:
			return git.Repo(target);
		except git.InvalidGitRepositoryError:
			return False;