Contribute to One Love
======================

### Git workflow

Fork this repo and create feature branch for every feature. When done, submit
a pull request.

__Branch naming__

Branch name should reflect feature name. If using multiple words, use dash
(`-`) as delimiter. Also, include prefix `feature`, `bug`, `refactor` in branch
name, followed by slash (`/`).

_Correct:_

- `feature/feature-name`

_Incorrect:_

- `feature-name`
- `feature/feature_name`
- `feature/featureName`

__Commits:__

Commits should be atomic - the smaller they are, the better it gets.

__Commit messages:__

Start your commit message with capital letter.
First line should be commit description, no longer than 65 characters.
If you work on one of the issues, include issue number in your commit summary.
If what you have to say about the commit exceeds 65 characters, insert blank
line under summary and write the rest of the message, just make sure lines
don't exceed 80 characters.

_Correct:_

    Adds awesome feature to supermodule #442.

or:

    Adds awesome feature to supermodule #442.

    The rest of the message can be as long as you want
    spanning across multiple lines.

__Merging pull requests:__

Make sure pull request passes all tests and always use Github's web interface
to do the merge. If merge isn't possible, rebase local branch on master,
resolve any conflicts that might happen and do a forced push to remote feature
branch. After that, use web interface to merge pull request. Always delete
remote feature branch after merge.

__IMPORTANT:__ Never push to master branch, even if your access rights permit
that.

### Naming conventions

__Files:__

When naming files and directories, always use lowercase lettes and underscode
(`_`) as delimiter.

_Correct:_

- `file_name.ext`

_Incorrect:_

- `fileName.ext`
- `file-name.ext`


### Testing requirements

Test it, don't guess it. Cover all features you make with unit tests.
If refactoring, make sure tests pass, otherwise your pull request won't be
accepted.

In order to run a test. Run the following command in the repo directory.

    $ docker-compose run --rm backend bin/test.sh

When the testing is finished you can get one of the following results:

  - . test passed
  - F your test failed
  - E something really bad happend



### Coding style

__Indentation:__

Use spaces for indentation, never tabs. Configure your editor to use soft tabs
(or translate tabs to spaces, as labeled in some editors). Set it to 4 spaces
per tab.

__Python:__

One Love API uses [PEP8](http://legacy.python.org/dev/peps/pep-0008/) compatible coding style, plus some extras. For example,
if arguments of function/class call excede 80 characters, every argument has
its own line

_Correct:_

`some_func(short='arguments')`
```
some_func(
    long='arguments',
    short='lines',
)
```

_Incorrect:_
```
some_func(arg1=1, arg2=2,
  arg3=3, arg4=4
)
```
