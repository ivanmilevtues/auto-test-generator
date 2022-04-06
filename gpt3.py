import openai

openai.api_key = "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"

code =  "Module(body=[ClassDef(name='TestableClass', bases=[], keywords=[], body=[FunctionDef(name='__init__', args=arguments(posonlyargs=[], args=[arg(arg='self'), arg(arg='a'), arg(arg='b')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Assign(targets=[Attribute(value=Name(id='self', ctx=Load()), attr='a', ctx=Store())], value=Name(id='a', ctx=Load())), Assign(targets=[Attribute(value=Name(id='self', ctx=Load()), attr='b', ctx=Store())], value=Name(id='b', ctx=Load()))], decorator_list=[]), FunctionDef(name='sum', args=arguments(posonlyargs=[], args=[arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Return(value=BinOp(left=Attribute(value=Name(id='self', ctx=Load()), attr='a', ctx=Load()), op=Add(), right=Attribute(value=Name(id='self', ctx=Load()), attr='b', ctx=Load())))], decorator_list=[])], decorator_list=[])], type_ignores=[])"
test = "Module(body=[Import(names=[alias(name='unittest')]), ImportFrom(module='TestableClass', names=[alias(name='TestableClass')], level=0), ClassDef(name='TestSum', bases=[Attribute(value=Name(id='unittest', ctx=Load()), attr='TestCase', ctx=Load())], keywords=[], body=[FunctionDef(name='test_sum', args=arguments(posonlyargs=[], args=[arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Assign(targets=[Name(id='tc', ctx=Store())], value=Call(func=Name(id='TestableClass', ctx=Load()), args=[Constant(value=4), Constant(value=2)], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='self', ctx=Load()), attr='assertEqual', ctx=Load()), args=[Call(func=Attribute(value=Name(id='tc', ctx=Load()), attr='sum', ctx=Load()), args=[], keywords=[]), Constant(value=6), Constant(value='Should be 6')], keywords=[]))], decorator_list=[]), FunctionDef(name='test_sum_tuple', args=arguments(posonlyargs=[], args=[arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Assign(targets=[Name(id='tc', ctx=Store())], value=Call(func=Name(id='TestableClass', ctx=Load()), args=[UnaryOp(op=USub(), operand=Constant(value=2)), Constant(value=2)], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='self', ctx=Load()), attr='assertEqual', ctx=Load()), args=[Call(func=Attribute(value=Name(id='tc', ctx=Load()), attr='sum', ctx=Load()), args=[], keywords=[]), Constant(value=0), Constant(value='Should be 0')], keywords=[]))], decorator_list=[])], decorator_list=[]), If(test=Compare(left=Name(id='__name__', ctx=Load()), ops=[Eq()], comparators=[Constant(value='__main__')]), body=[Expr(value=Call(func=Attribute(value=Name(id='unittest', ctx=Load()), attr='main', ctx=Load()), args=[], keywords=[]))], orelse=[])], type_ignores=[])"


response = openai.Completion.create(
  engine="code-davinci-002",
  prompt="""### Python 3
  #
  # Module(body=[ClassDef(name='TestableClass', bases=[], keywords=[], body=[FunctionDef(name='__init__', args=arguments(posonlyargs=[], args=[arg(arg='self'), arg(arg='a'), arg(arg='b')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Assign(targets=[Attribute(value=Name(id='self', ctx=Load()), attr='a', ctx=Store())], value=Name(id='a', ctx=Load())), Assign(targets=[Attribute(value=Name(id='self', ctx=Load()), attr='b', ctx=Store())], value=Name(id='b', ctx=Load()))], decorator_list=[]), FunctionDef(name='sum', args=arguments(posonlyargs=[], args=[arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Return(value=BinOp(left=Attribute(value=Name(id='self', ctx=Load()), attr='a', ctx=Load()), op=Add(), right=Attribute(value=Name(id='self', ctx=Load()), attr='b', ctx=Load())))], decorator_list=[])], decorator_list=[])], type_ignores=[])
  #
  ### A unittest test which tests the sum method
  class Test:
""",
  temperature=0,
  max_tokens=150,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["#", "\"\"\""]
)
print(response)