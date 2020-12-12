import calculate

text = input('calculate > ')
result, error = calculate.run('<stdin>', text)
print(result)
