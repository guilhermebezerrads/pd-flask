unidades_academicas = ['UFMG', '(DCC) CIÊNCIA DA COMPUTAÇÃO','(EE) ESCOLA DE ENGENHARIA', 
'(ICEX) INSTITUTO DE CIÊNCIAS EXATAS', 'INSTITUTO DE CIÊNCIAS BIOLÓGICAS', 
'INSTITUTO DE GEOCIÊNCIAS', 'ESCOLA DE ARQUITETURA', 'ESCOLA DE BELAS ARTES', 
'ESCOLA DE CIÊNCIA DA INFORMAÇÃO', 'ESCOLA DE EDUCAÇÃO FÍSICA, FISIOTERAPIA.E TERAPIA OCUPACIONAL',
'ESCOLA DE ENFERMAGEM', 'ESCOLA DE MÚSICA', 'ESCOLA DE VETERINÁRIA', 'ESPORTES', 'ESTATÍSTICA',
'ESTUDOS SOCIAIS', 'FACULDADE CIÊNCIAS ECONÔMICAS', 'FACULDADE DE DIREITO', 'FACULDADE DE EDUCAÇÃO',
'FACULDADE DE FARMACIA', 'FACULDADE DE FARMÁCIA', 'FACULDADE DE FILOSOFIA E CIÊNCIAS HUMANAS', 
'FACULDADE DE LETRAS', 'FACULDADE DE MEDICINA', 'FACULDADE DE ODONTOLOGIA']

def lista_unidades_academicas():
    lista = []
    i = 0
    for unidade in unidades_academicas:
        lista.append((str(i), unidade))
        i = i+1
    
    return lista


todos_departamentos = ['(DCC) CIÊNCIA DA COMPUTAÇÃO','(EE) ESCOLA DE ENGENHARIA', '(ICEX) INSTITUTO DE CIÊNCIAS EXATAS', 'INSTITUTO DE CIÊNCIAS BIOLÓGICAS', 'INSTITUTO DE GEOCIÊNCIAS', 'ESCOLA DE ARQUITETURA', 'ESCOLA DE BELAS ARTES', 'ESCOLA DE CIÊNCIA DA INFORMAÇÃO', 'ESCOLA DE EDUCAÇÃO FÍSICA, FISIOTERAPIA.E TERAPIA OCUPACIONAL',
'ESCOLA DE ENFERMAGEM', 'ESCOLA DE MÚSICA', 'ESCOLA DE VETERINÁRIA', 'ESPORTES', 'ESTATÍSTICA'
'ESTUDOS SOCIAIS', 'FACULDADE CIÊNCIAS ECONÔMICAS', 'FACULDADE DE DIREITO', 'FACULDADE DE EDUCAÇÃO',
'FACULDADE DE FARMACIA', 'FACULDADE DE FARMÁCIA', 'FACULDADE DE FILOSOFIA E CIÊNCIAS HUMANAS', 'FACULDADE DE LETRAS', 'FACULDADE DE MEDICINA', 'FACULDADE DE ODONTOLOGIA', 
'ENGENHARIA DE ESTRUTURAS', 'ENGENHARIA DE MINAS', 'ENGENHARIA DE PRODUÇÃO', 'ENGENHARIA DE TRANSPORTES E GEOTECNIA', 'ENGENHARIA ELETRÔNICA', 'ENGENHARIA ELÉTRICA', 'ENGENHARIA HIDRAULICA', 'ENGENHARIA HIDRÁULICA E RECURSOS HÍDRICOS', 'ENGENHARIA INDUSTRIAL', 'ENGENHARIA MECÂNICA', 'ENGENHARIA METALÚRGICA', 'ENGENHARIA METALÚRGICA E DE MATERIAIS', 'ENGENHARIA NUCLEAR', 'ENGENHARIA QUÍMICA', 'ENGENHARIA RURAL-NTCA', 'ENGENHARIA SANITÁRIA E AMBIENTAL', 'ENGENHARIA TERMICA', 'ENGENHARIA VIAS COMUNIC.TRANSP', 'ELETRONICA', 'ENGENHARIA CONSTRUCAO DE MAQUI', 

'ADMINISTRACAO-NTCA', 'ADMINISTRAÇÃO ESCOLAR', 'ALIMENTOS', 'ANATOMIA E IMAGEM', 
'ANATOMIA PATOLÓGICA E MEDICINA LEGAL', 'ANTROPOLOGIA E ARQUEOLOGIA', 
'ANÁLISE CRITICA E HISTÓRICA DA ARQUITERURA E DO URBANISMO', 'ANÁLISES CLINICAS E TOXICOLÓGICAS',
'ARTES CÊNICAS', 'ARTES PLÁSTICAS', 'BIBLIOGRAFIA E DOCUMENTACAO', 'BIBLIOTECONOMIA',
'BIOLOGIA', 'BIOLOGIA APLICADA', 'BIOLOGIA GERAL', 'BIOQUÍMICA E IMUNOLOGIA', 'BOTÂNICA', 'CARTOGRAFIA',
'CENTRO DE ALFABETIZAÇÃO, LEITURA E ESCRITA', 'CENTRO DE AQUISIÇÃO E PROCESSAMENTO DE IMAGENS',
'CENTRO DE BIOTERISMO', 'CENTRO DE COLEÇÕES TAXONÔMICAS', 'CENTRO DE CONSERVAÇÃO E RESTAURAÇÃO DE BENS CULTURAIS MÓVEIS',
'CENTRO DE DESENVOLVIMENTO E PLANEJAMENTO REGIONAL', 'CENTRO DE ENSINO DE CIÊNCIAS E MATEMÁTICA', 'CENTRO DE ESTUDOS LITERÁRIOS E CULTURAIS',
'CENTRO DE ESTUDOS MINEIROS', 'CENTRO DE ESTUDOS PORTUGUESES', 'CENTRO DE MUSICALIZAÇÃO INTEGRADA', 
'CENTRO DE PESQUISA EM MÚSICA CONTEMPORÂNEA', 'CENTRO DE PESQUISA PROFESSOR MANOEL TEIXEIRA DA COSTA', 'CENTRO DE PESQUISAS QUANTITATIVAS EM CIÊNCIAS SOCIAIS',
'CENTRO DE TECNOLOGIA EDUCACIONAL EM ENFERMAGEM', 'CENTRO DE TREINAMENTO ESPORTIVO', 'CENTRO PEDAGÓGICO',
'CIENCIAS', 'CIENCIAS SOCIAIS', 'CIRURGIA', 'CIÊNCIA POLÍTICA', 'CIÊNCIAS ADMINISTRATIVAS', 'CIÊNCIAS APLICADAS A EDUCAÇÃO', 'CIÊNCIAS CONTÁBEIS',
'CIÊNCIAS ECONÔMICAS', 'CLINICA, PATOLOGIA E CIRURGIAS ODONTOLÓGICAS', 'CLÍNICA E CIRURGIA VETERINÁRIAS',
'CLÍNICA MÉDICA', 'COLÉGIO TÉCNICO', 'COMPUTACAO E ESTATISTICA', 'COMUNICACAO E EXPRESSAO', 'COMUNICACAO E EXPRESSAO-NTCA',
'COMUNICAÇÃO SOCIAL', 'DEMOGRAFIA', 'DESENHO', 'DIREITO DE PROCESSO CIVIL E COMERCIAL', 'DIREITO DO TRABALHO E INTRODUÇÃO AO ESTUDO DO DIREITO',
'DIREITO E PROCESSO PENAL', 'DIREITO PÚBLICO', 'DIRETORIA CENTRO PEDAGÓGICO', 'DIRETORIA COLÉGIO TÉCNICO', 'DIRETORIA FACULDADE DE LETRAS',
'DIRETORIA ICA', 'DIRETORIA TEATRO UNIVERSITÁRIO', 'DIVISÃO DE ASSISTÊNCIA JUDICIÁRIA', 'EDUCACAO ARTISTICA', 'EDUCACAO FISICA (2208)',
'EDUCACAO FISICA (2303)', 'EDUCAÇÃO FÍSICA', 'ENFERMAGEM APLICADA', 'ENFERMAGEM BÁSICA', 'ENFERMAGEM MATERNO-INFANTIL E SAÚDE PÚBLICA', 
'FACULDADE DE FARMÁCIA', 'FACULDADE DE FILOSOFIA E CIÊNCIAS HUMANAS', 'FACULDADE DE LETRAS', 'FACULDADE DE MEDICINA', 'FACULDADE DE ODONTOLOGIA', 
'FARMACOLOGIA', 'FARMÁCIA SOCIAL', 'FAZENDA EXPERIMENTAL PROFESSOR HÉLIO BARBOSA', 'FILOSOFIA', 'FISICA (2309)', 'FISIOLOGIA E BIOFÍSICA', 'FISIOTER. E TER. OCUPACIONAL', 'FISIOTERAPIA', 'FITOTECNICA-NTCA',
'FONOAUDIOLOGIA', 'FORMACAO ESPECIAL', 'FOTOGRAFIA E CINEMA', 'FÍSICA', 'GEOGRAFIA', 'GEOLOGIA', 'GINECOLOGIA E OBSTETRÍCIA', 
'HISTÓRIA', 'HOSPITAL DAS CLÍNICAS', 'HOSPITAL VETERINÁRIO', 'INSTITUTO CASA DA GLÓRIA', 'INSTITUTO DE CIÊNCIAS AGRÁRIAS',
'INSTITUTO DE GEOCIÊNCIAS', 'INSTRUMENTACAO', 'INSTRUMENTOS E CANTO', 'LETRAS', 'LETRAS ANGLO-GERMANICAS', 'LETRAS CLASSICAS',
'LETRAS ROMANICAS', 'LETRAS VERNACULAS', 'LINGUISTICA', 'LINGUISTICA E TEORIA DA LITERA', 'MATEMATICA (2207)', 'MATEMATICA (2311)',
'MATEMÁTICA', 'MATERIAIS E DA CONSTR. CIVIL', 'MEDICINA PREVENTIVA E SOCIAL', 'MEDICINA VETERINÁRIA PREVENTIVA', 'METODOS E TÉCNICAS DE ENSINO', 'MICROBIOLOGIA', 'MORFOLOGIA', 'NUTRIÇÃO',
'NÚCLEO DE AÇÕES E PESQUISA EM APOIO DIAGNÓSTICO', 'NÚCLEO DE EDUCAÇÃO EM SAÚDE COLETIVA', 'ODONTOLOGIA RESTAURADORA', 'ODONTOLOGIA SOCIAL E PREVENTIVA',
'ODONTOPEDIATRIA E ORTODONTIA', 'OFTALM.OTORRINOLAR.FONOAUDIOL.', 'OFTALMOLOGIA E OTORRINOLARINGOLOGIA', 'OFTALMOLOGIA, OTORRINOLARINGOLOGIA E FONOAUDIOLOGIA',
'ORGANIZAÇÃO E TRATAMENTO DA INFORMAÇÃO', 'PARASITOLOGIA', 'PATOLOGIA GERAL', 'PEDIATRIA', 'PLANEJAMENTO ARQUITETONICO',
'PRATICA DE EDUCAÇÃO FÍSICA', 'PRODUTOS FARMACÊUTICOS', 'PROJETOS', 'PROPEDÊUTICA COMPLEMENTAR', 'PSICOLOGIA', 'PSIQUIATRIA E NEUROLOGIA',
'QUIMICA (2306)', 'QUIMICA APLICADA', 'QUIMICA-NTCA', 'QUÍMICA', 'REPRESENT.GRAF. E EXPRES. ARQ.', 'REUNI', 'SAÚDE MENTAL',
'SEMIOT. E TEORIA DA LITERATURA', 'SERIES INICIAIS', 'SOCIOLOGIA', 'SOCIOLOGIA E ANTROPOLOGIA', 'TEATRO UNIVERSITARIO (2501)',
'TEATRO UNIVERSITÁRIO', 'TECNICAS GERAIS', 'TECNICAS MEDICAS', 'TECNOLOGIA DO DESIGN, DA ARQUITETURA E DO URBANISMO',
'TECNOLOGIA E INSPEÇÃO DE PRODUTOS DE ORIGEM ANIMAL', 'TECNOLOGIA FARMACEUTICA', 'TEORIA E GESTÃO DA INFORMAÇÃO', 
'TEORIA GERAL DA MÚSICA', 'TERAPIA OCUPACIONAL', 'UFMG', 'URBANISMO', 'ZOOLOGIA', 'ZOOTECNIA', 'ZOOTECNIA-NTCA']