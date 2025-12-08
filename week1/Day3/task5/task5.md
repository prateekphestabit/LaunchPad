##Git Stash — Save Work Temporarily Without Committing

git stash lets you hide your uncommitted changes so you can switch branches without losing anything.

#When should you use stash?

You’re in the middle of work but need to switch branches quickly

You want to test something on another branch

You want to clean your working directory temporarily

🛠️ Stash workflow
1. Save current uncommitted changes
git stash


or save with a message:

git stash push -m "WIP: fixing login bug"


Your working directory becomes clean.

2. See your stashes
git stash list

3. Apply the latest stash
git stash apply

4. Apply a specific stash
git stash apply stash@{2}

5. Apply and delete stash
git stash pop

6. Delete a stash
git stash drop stash@{1}

7. Clear all stashes
git stash clear
