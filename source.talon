{
"5 + true;",
"type mismatch: INTEGER + BOOLEAN",
},
{
"5 + true; 5;",
"type mismatch: INTEGER + BOOLEAN",
},
{
"-true",
"unknown operator: -BOOLEAN",
},
{
"true + false;",
"unknown operator: BOOLEAN + BOOLEAN",
},
{
"5; true + false; 5",
"unknown operator: BOOLEAN + BOOLEAN",
},
{
"if (10 > 1) { true + false; }",
"unknown operator: BOOLEAN + BOOLEAN",
},