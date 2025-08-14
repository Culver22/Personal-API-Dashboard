import pytest
from pydantic import ValidationError
from app.models.goal import CreateGoal, ReadGoal
from app.models.todo import CreateTodo, ReadTodo, Priority
from app.models.workout import CreateWorkout, ReadWorkout, WorkoutType

''' GOAL MODEL TESTS '''


# Test 1: Valid CreateGoal
def test_create_goal_valid():
    goal = CreateGoal(title="Learn FastAPI", description="Follow tutorial", deadline="2025-09-01", completed=False)
    assert goal.title == "Learn FastAPI"
    assert goal.completed is False


# Test 2: Missing required 'title'
def test_create_goal_missing_title():
    with pytest.raises(ValidationError):
        CreateGoal(description="Missing title")


# Test 3: Empty description is allowed
def test_create_goal_empty_description():
    goal = CreateGoal(title="Read", description="", deadline="2025-09-01")
    assert goal.description == ""


# Test 4: Deadline is optional
def test_create_goal_no_deadline():
    goal = CreateGoal(title="Stretch", description="Daily habit")
    assert goal.deadline is None


# Test 5: Completed must be a boolean
def test_create_goal_invalid_completed_type():
    with pytest.raises(ValidationError):
        CreateGoal(title="Workout", completed="yes")  # should be boolean


# Test 6: ReadGoal inherits CreateGoal and includes ID
def test_read_goal_valid():
    goal = ReadGoal(id=1, title="Stretch", description="Daily", deadline="2025-08-14", completed=False)
    assert goal.id == 1
    assert isinstance(goal, CreateGoal)



''' TODO MODEL TESTS '''


# Test 7: Valid CreateTodo with priority
def test_create_todo_valid():
    todo = CreateTodo(title="Buy milk", description="Almond milk", priority=Priority.HIGH, completed=False)
    assert todo.priority == Priority.HIGH


# Test 8: Invalid priority (not a valid enum)
def test_create_todo_invalid_priority():
    with pytest.raises(ValidationError):
        CreateTodo(title="Buy milk", priority="urgent")  # invalid enum


# Test 9: ReadTodo inherits CreateTodo and includes ID
def test_read_todo_valid():
    todo = ReadTodo(id=3, title="Laundry", completed=True, priority=Priority.LOW)
    assert todo.id == 3
    assert todo.priority == Priority.LOW

# Test 10: Missing required title
def test_create_todo_missing_title():
    with pytest.raises(ValidationError):
        CreateTodo(description="No title")


# Test 11: Empty title string
def test_create_todo_empty_title():
    todo = CreateTodo(title="", description="Empty title test")
    assert todo.title == ""


# Test 12: Priority is optional
def test_create_todo_priority_optional():
    todo = CreateTodo(title="Walk dog")
    assert todo.priority is None


# Test 13: Completed defaults to False
def test_create_todo_completed_default():
    todo = CreateTodo(title="Do dishes")
    assert todo.completed is False


# Test 14: Invalid type for completed
def test_create_todo_invalid_completed_type():
    with pytest.raises(ValidationError):
        CreateTodo(title="Clean", completed="done")  # should be bool

