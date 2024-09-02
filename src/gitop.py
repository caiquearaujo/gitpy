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

	def exists (self):
		return self.repo != False;

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

	def commit(self, message: str, date: str = 'now'):
		self.git.add('--all');

		if ( date == 'now' ):
			self.git.commit('-m', message);
		else:
			self.git.commit('--date', date, '-m', message);

	def checkout(self, branch: str):
		self.git.checkout(branch);

	def merge(self, branch: str, message: str):
		self.git.merge(branch, '-m', message);

	def delete(self, branch: str, remote: str = 'origin'):
		self.git.branch('-d', branch);
		self.git.push(remote, '--delete', branch);

	def currentBranch(self):
		branch = self.git.branch('--show-current');
		Terminal.warning("Working branch: " + branch);
		return branch;

	def hasUncommitedChanges(self):
		return self.repo.is_dirty(untracked_files=True);

	@staticmethod
	def status (target):
		try:
			return git.Repo(target, search_parent_directories=True);
		except git.InvalidGitRepositoryError:
			return False;