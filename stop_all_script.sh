
echo "Stopping all jarvis function"
ps ax | grep 'python auto*' | grep -v grep | awk '{print $1}' | xargs kill
echo "All jarvis services were stopped"
