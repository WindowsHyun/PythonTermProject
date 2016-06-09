#include "python.h" 

static PyObject *

txtOut_save( PyObject *self, PyObject *args )
{
	const char* str = NULL;
	int len;

	if ( !PyArg_ParseTuple( args, "s", &str ) ) // 매개변수 값을 분석하고 지역변수에 할당 시킵니다.
		return NULL;


	FILE *f;
	f = fopen( "Information MiniDust.txt", "w" );
	len = strlen( str );
	fprintf( f, str );
	fclose( f );

	return Py_BuildValue( "i", len );
}

static PyMethodDef txtOutMethods[] = {
	{ "txtOut", txtOut_save, METH_VARARGS,
	"save the txt File" },
	{ NULL, NULL, 0, NULL }    //배열의 끝을 나타낸다.
};


static struct PyModuleDef txtOutmodule = {
	PyModuleDef_HEAD_INIT,
	"txtOut",            // 모듈 이름
	"Take a string and then saved as a txt file.", // 모듈 설명을 적는 `, 모듈의 __doc__에 저장됩니다.
	-1,txtOutMethods
};

PyMODINIT_FUNC
PyInit_txtOut( void )
{
	return PyModule_Create( &txtOutmodule );
}
