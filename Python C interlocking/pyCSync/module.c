#include "python.h" 

static PyObject *

txtOut_save( PyObject *self, PyObject *args )
{
	const char* str = NULL;
	int len;

	if ( !PyArg_ParseTuple( args, "s", &str ) ) // �Ű����� ���� �м��ϰ� ���������� �Ҵ� ��ŵ�ϴ�.
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
	{ NULL, NULL, 0, NULL }    //�迭�� ���� ��Ÿ����.
};


static struct PyModuleDef txtOutmodule = {
	PyModuleDef_HEAD_INIT,
	"txtOut",            // ��� �̸�
	"Take a string and then saved as a txt file.", // ��� ������ ���� `, ����� __doc__�� ����˴ϴ�.
	-1,txtOutMethods
};

PyMODINIT_FUNC
PyInit_txtOut( void )
{
	return PyModule_Create( &txtOutmodule );
}
