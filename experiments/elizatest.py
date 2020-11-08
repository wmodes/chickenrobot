import eliza

therapist = eliza.Eliza()
while some_condition:
  input = prompt("> ")
  reply = therapist.respond(input)
  print(reply)
