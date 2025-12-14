prateek@HESTABIT-301:~/Prateek/LaunchPad$ git checkout release/v0.1
Switched to branch 'release/v0.1'
Your branch is up to date with 'origin/release/v0.1'.

prateek@HESTABIT-301:~/Prateek/LaunchPad$ git cherry-pick 158ffb3
Auto-merging week1/Day3/task1/task1.txt
CONFLICT (content): Merge conflict in week1/Day3/task1/task1.txt
error: could not apply 158ffb3... syntax error
hint: After resolving the conflicts, mark them with
hint: "git add/rm <pathspec>", then run
hint: "git cherry-pick --continue".
hint: You can instead skip this commit with "git cherry-pick --skip".
hint: To abort and get back to the state before "git cherry-pick",
hint: run "git cherry-pick --abort".

prateek@HESTABIT-301:~/Prateek/LaunchPad$ git push
Everything up-to-date

prateek@HESTABIT-301:~/Prateek/LaunchPad$ git status
On branch release/v0.1
Your branch is up to date with 'origin/release/v0.1'.

You are currently cherry-picking commit 158ffb3.
  (all conflicts fixed: run "git cherry-pick --continue")
  (use "git cherry-pick --skip" to skip this patch)
  (use "git cherry-pick --abort" to cancel the cherry-pick operation)

nothing to commit, working tree clean

prateek@HESTABIT-301:~/Prateek/LaunchPad$ git cherry-pick --continue
On branch release/v0.1
Your branch is up to date with 'origin/release/v0.1'.

You are currently cherry-picking commit 158ffb3.
  (all conflicts fixed: run "git cherry-pick --continue")
  (use "git cherry-pick --skip" to skip this patch)
  (use "git cherry-pick --abort" to cancel the cherry-pick operation)

nothing to commit, working tree clean
The previous cherry-pick is now empty, possibly due to conflict resolution.
If you wish to commit it anyway, use:

    git commit --allow-empty

Otherwise, please use 'git cherry-pick --skip'
prateek@HESTABIT-301:~/Prateek/LaunchPad$ 