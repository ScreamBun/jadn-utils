from jadnutils.gv.gv_generator import GvGenerator

schema = {
    'meta': {'roots': ['Album']},
    'types': [
        ['Album', 'Record', [], '', [['id','id','String',[]], ['tracks','tracks','Array', ['*Track']]]],
        ['Track', 'Record', [], '', [['title','title','String',[]]]],
        ['String', 'String', [], '', []]
    ]
}

gv = GvGenerator(schema)
print(gv.generate())
