# Modern To-Do List Application

A beautiful and interactive To-Do List manager created with Python and Tkinter.

![To-Do List App](https://via.placeholder.com/800x450.png?text=Modern+To-Do+List+Application)

## Features

- Modern, responsive user interface with elegant styling
- Add, edit, and delete tasks with ease
- Mark tasks as complete/incomplete with visual indicators
- Set task priorities (High, Medium, Low) with color coding
- Filter tasks by status (All, Active, Completed, High Priority)
- Right-click context menu for quick actions
- Placeholder text in the input field for better UX
- Interactive buttons with hover effects
- Color-coded tasks based on priority level
- Tasks automatically sorted by priority and completion status
- Clear all tasks at once
- Tasks automatically saved between sessions
- User-friendly GUI interface
- Keyboard shortcuts for increased productivity

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)

## How to Run

1. Make sure you have Python installed on your system
2. Clone or download this repository
3. Run the application:

```
python todo_app.py
```

or

```
./run_todo.sh
```

## Usage Instructions

- **Add a task**: Type your task in the entry field, select priority, and click "Add Task" or press Enter
- **Mark as complete**: Select a task and click "Mark Complete" or use right-click menu
- **Edit a task**: Select a task and click "Edit Task" or double-click on the task
- **Delete a task**: Select a task and click "Delete Task" or use right-click menu
- **Filter tasks**: Use the dropdown filter to show All, Active, Completed, or High Priority tasks
- **Set priority**: Change priority when creating or editing a task, or use the right-click menu
- **Clear all tasks**: Click "Clear All" (will prompt for confirmation)

## Task Priorities

Tasks are color-coded by priority:
- **High priority**: Light red background with "!" indicator
- **Medium priority**: Light yellow background with "●" indicator
- **Low priority**: Light green background with "○" indicator

The application automatically sorts tasks by completion status and priority level, with active high priority tasks appearing at the top of the list.

## Keyboard Shortcuts

- **Enter**: Add a new task (when focus is in the entry field)
- **Double-click**: Edit the selected task
- **Enter**: Save changes (when editing a task)
- **Right-click**: Open context menu with task options

## Data Storage

All tasks are saved in a `tasks.json` file in the same directory as the application. This allows your tasks to persist between application sessions.

## Interactive Elements

- **Hover effects**: Buttons change color when hovered over
- **Input field**: Shows placeholder text when empty
- **Context menu**: Right-click on a task to see available actions
- **Filtered views**: Easily switch between different task views
- **Visual feedback**: Clear indicators for task status and priority 