import turtle

# Set up the turtle
turtle.penup()
turtle.goto(0, 0)
turtle.pendown()
turtle.pensize(2)
turtle.color("black")

# Draw the ruler
for i in range(10):
    turtle.forward(10)
    turtle.penup()
    turtle.goto(turtle.xcor(), turtle.ycor() - 5)
    turtle.pendown()

# Finish up
turtle.hideturtle()
turtle.done()
