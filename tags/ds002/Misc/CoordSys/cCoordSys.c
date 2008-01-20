/* 	$Id: cCoordSys.c,v 1.11 2003-04-17 09:32:58 joerg Exp $	 */

#include <math.h>
#include <float.h>
#include <Python.h>

#define DNDEF DBL_MAX
#define INDEF INT_MAX

#ifndef CSYSVERSION
#define CSYSVERSION 0.0
#endif

static double *vCross(double *a, double *b, double *r) {
  r[0] = a[1]*b[2]-a[2]*b[1];
  r[1] = a[2]*b[0]-a[0]*b[2];
  r[2] = a[0]*b[1]-a[1]*b[0];
  return r;
}

static double *vDiff(double *a, double *b, double *r) {
  r[0] = a[0]-b[0];
  r[1] = a[1]-b[1];
  r[2] = a[2]-b[2];
  return r;
}

static double *vAdd(double *a, double *b, double *r) {
  r[0] = a[0]+b[0];
  r[1] = a[1]+b[1];
  r[2] = a[2]+b[2];
  return r;
}

static double *vNorm(double *a) {
  double mag = sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2]);
  if (mag > 0.0) {
    a[0] /= mag; 
    a[1] /= mag; 
    a[2] /= mag;
  }
  return a;
}

static double *vMult(double *a, double mag) {
  a[0] *= mag;
  a[1] *= mag;
  a[2] *= mag;
  return a;
}

static double *vCopy(double *a, double *b) {
  b[0] = a[0];
  b[1] = a[1];
  b[2] = a[2];
  return b;
}

static double vLen(double *a) {
  return sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2]);
}

static int solve3x3(double *A, double *b, double *x) {
  double det;
#define A(row,col) A[col+3*row] /* row-col to linear mapping */ 
  det = (A(0,0)*A(1,1)*A(2,2) + A(0,1)*A(1,2)*A(2,0)+
	 A(0,2)*A(1,0)*A(2,1) - A(0,2)*A(1,1)*A(2,0)-
	 A(0,0)*A(1,2)*A(2,1) - A(0,1)*A(1,0)*A(2,2));
  if (det != 0) {
    x[0] = (b[0]*A(1,1)*A(2,2) + A(0,1)*A(1,2)*b[2]+
	    A(0,2)*b[1]*A(2,1) - A(0,2)*A(1,1)*b[2]-
	    b[0]*A(1,2)*A(2,1) - A(0,1)*b[1]*A(2,2))/det;
    x[1] = (A(0,0)*b[1]*A(2,2) + b[0]*A(1,2)*A(2,0)+
	    A(0,2)*A(1,0)*b[2] - A(0,2)*b[1]*A(2,0)-
	    A(0,0)*A(1,2)*b[2] - b[0]*A(1,0)*A(2,2))/det;
    x[2] = (A(0,0)*A(1,1)*b[2] + A(0,1)*b[1]*A(2,0)+
	    b[0]*A(1,0)*A(2,1) - b[0]*A(1,1)*A(2,0)-
	    A(0,0)*b[1]*A(2,1) - A(0,1)*A(1,0)*b[2])/det;
#undef A 
    return 1;
  } else
    return 0;
}

static PyObject *vec2tuple(double *v) {
  PyObject *T = PyTuple_New(3);
  PyTuple_SetItem(T, 0, PyFloat_FromDouble(v[0]));
  PyTuple_SetItem(T, 1, PyFloat_FromDouble(v[1]));
  PyTuple_SetItem(T, 2, PyFloat_FromDouble(v[2]));
  return T;
}

static PyObject *vec2tuple2(double *v) {
  PyObject *T = PyTuple_New(2);
  PyTuple_SetItem(T, 0, PyFloat_FromDouble(v[0]));
  PyTuple_SetItem(T, 1, PyFloat_FromDouble(v[1]));
  return T;
}

static double *seq2vec(PyObject *T, double *v) {
  v[0] = PyFloat_AsDouble(PySequence_GetItem(T, 0));
  v[1] = PyFloat_AsDouble(PySequence_GetItem(T, 1));
  v[2] = PyFloat_AsDouble(PySequence_GetItem(T, 2));
  return v;
}

/* CoordSys */
typedef struct {
    PyObject_HEAD
    PyObject *attr;
    double o[3];
    double m[9];
    double tol2D;
} CoordSys;

staticforward PyTypeObject    CoordSys_Type;
staticforward PyMethodDef     CoordSys_Methods[];

/* general Exception */
static PyObject *CoordSysError;

/* some common exceptions ... */
#define ERR_ARG CoordSysError, "Wrong number or type of arguments"
#define ERR_CNV CoordSysError, "3D -> 2D conversion error"
#define ERR_INV CoordSysError, "Invalid conversion matrix - no solution found"
#define ERR_POL CoordSysError, "Invalid point list for 2D system"

/* raise an exception and return NULL */
static PyObject * CoordSys_Raise(PyObject *e, char *msg) {
    PyErr_SetString(e, msg);
    return NULL;
}

#define CoordSys_Check(o) ((o)->ob_type == &CoordSys_Type)

static PyObject *CoordSys_new(PyObject *self, PyObject *args) {
    PyObject *O=NULL, *U=NULL, *V=NULL, *W=NULL;
    CoordSys *c = PyObject_NEW(CoordSys, &CoordSys_Type);
    c->tol2D = DNDEF;
    c->attr  = NULL;
    if (! PyArg_ParseTuple(args, "|OOOO", &O, &U, &V, &W))
	return CoordSys_Raise(ERR_ARG);
    if (O) {
	if (PySequence_Check(O)) {
	    if (PySequence_Length(O) != 3)
		return CoordSys_Raise(ERR_ARG);
	    seq2vec(O, c->o);
	}
    } else {
	c->o[0] = 0.0; c->o[1] = 0.0; c->o[2] = 0.0;
    }
    if (U) {
	if (PySequence_Check(U)) {
	    if (PySequence_Length(U) != 3)
		return CoordSys_Raise(ERR_ARG);
	    c->m[0] = PyFloat_AsDouble(PySequence_GetItem(U, 0));
	    c->m[3] = PyFloat_AsDouble(PySequence_GetItem(U, 1));
	    c->m[6] = PyFloat_AsDouble(PySequence_GetItem(U, 2));
	}
    } else {
	c->m[0] = 1.0; c->m[3] = 0.0; c->m[6] = 0.0;
    }
    if (V) {
	if (PySequence_Check(V)) {
	    if (PySequence_Length(V) != 3)
		return CoordSys_Raise(ERR_ARG);
	    c->m[1] = PyFloat_AsDouble(PySequence_GetItem(V, 0));
	    c->m[4] = PyFloat_AsDouble(PySequence_GetItem(V, 1));
	    c->m[7] = PyFloat_AsDouble(PySequence_GetItem(V, 2));
	}
    } else {
	c->m[1] = 0.0; c->m[4] = 1.0; c->m[7] = 0.0;
    }
    if (W) {
	if (PySequence_Check(W)) {
	    if (PySequence_Length(W) != 3)
		return CoordSys_Raise(ERR_ARG);
	    c->m[2] = PyFloat_AsDouble(PySequence_GetItem(W, 0));
	    c->m[5] = PyFloat_AsDouble(PySequence_GetItem(W, 1));
	    c->m[8] = PyFloat_AsDouble(PySequence_GetItem(W, 2));
	}
    } else {
	c->m[2] = 0.0; c->m[5] = 0.0; c->m[8] = 1.0;
    }
    if (PyErr_Occurred())
	return NULL;
    return (PyObject *)c;
}

static void CoordSys_dealloc(CoordSys *self) {
    Py_XDECREF(self->attr);
    PyObject_Del(self);
}

static PyObject *CoordSys_toGlobal(CoordSys *self, PyObject *L) {
    PyObject *LP, *G;
    double x, y, z, r[3];
    int i, l;
    if (! PySequence_Check(L))
	return CoordSys_Raise(ERR_ARG);
    l = PySequence_Length(L);
    G = PyTuple_New(l);
    for (i=0; i < l; i++) {
	LP = PySequence_GetItem(L, i);
	if (PySequence_Length(LP) < 2)
	    return CoordSys_Raise(ERR_ARG);
	x = PyFloat_AsDouble(PySequence_GetItem(LP, 0));
	y = PyFloat_AsDouble(PySequence_GetItem(LP, 1));
	if (PySequence_Length(LP) >= 3)
	    z = PyFloat_AsDouble(PySequence_GetItem(LP, 2));
	else
	    z = 0.0;
	r[0] = self->o[0] + x * self->m[0] + y * self->m[1] + z * self->m[2];
	r[1] = self->o[1] + x * self->m[3] + y * self->m[4] + z * self->m[5];
	r[2] = self->o[2] + x * self->m[6] + y * self->m[7] + z * self->m[8];
	PyTuple_SetItem(G, i, vec2tuple(r));
    }
    return G;
}

static PyObject *CoordSys_toLocal(CoordSys *self, PyObject *G) {
    PyObject *GP=NULL, *L;
    double g[3], b[3], x[3];
    int i, l;
    if (! PySequence_Check(G))
	return CoordSys_Raise(ERR_ARG);
    l = PySequence_Length(G);
    L = PyTuple_New(l);
    for (i=0; i < l; i++) {
	GP = PySequence_GetItem(G, i);
	if (PySequence_Length(GP) < 3)
	    return CoordSys_Raise(ERR_ARG);
	if (! solve3x3(self->m, vDiff(seq2vec(GP, g), self->o, b), x))
	    return CoordSys_Raise(ERR_INV);
	PyTuple_SetItem(L, i, vec2tuple(x));
    }
    return L;
}

static PyObject *CoordSys_toLocal2D(CoordSys *self, PyObject *G) {
    PyObject *GP=NULL, *L;
    double g[3], b[3], x[3];
    int i, l;
    if (! PySequence_Check(G))
	return CoordSys_Raise(ERR_ARG);
    l = PySequence_Length(G);
    L = PyTuple_New(l);
    for (i=0; i < l; i++) {
	GP = PySequence_GetItem(G, i);
	if (PySequence_Length(GP) < 3)
	    return CoordSys_Raise(ERR_ARG);
	if (! solve3x3(self->m, vDiff(seq2vec(GP, g), self->o, b), x))
	    return CoordSys_Raise(ERR_INV);
	if ((self->tol2D != DNDEF) && (fabs(x[2]) >= self->tol2D))
	    return CoordSys_Raise(ERR_CNV);
        PyTuple_SetItem(L, i, vec2tuple2(x));
    }
    return L;
}

static PyObject *CoordSys_matrix(CoordSys *self) {
    return Py_BuildValue("OOO", vec2tuple(self->m), vec2tuple(self->m+3), vec2tuple(self->m+6));
}

static PyObject *CoordSys_offset(CoordSys *self) {
    return vec2tuple(self->o);
}

static PyObject *CoordSys_u(CoordSys *self) {
    return Py_BuildValue("ddd",  self->m[0], self->m[3], self->m[6]);
}

static PyObject *CoordSys_v(CoordSys *self) {
    return Py_BuildValue("ddd",  self->m[1], self->m[4], self->m[7]);
}

static PyObject *CoordSys_w(CoordSys *self) {
    return Py_BuildValue("ddd",  self->m[2], self->m[5], self->m[8]);
}

static PyObject *CoordSys_set2DTol(CoordSys *self, PyObject *t) {
    if (! PyFloat_Check(t))
	self->tol2D = DNDEF;
    else
	self->tol2D = PyFloat_AsDouble(t);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *CoordSys_get2DTol(CoordSys *self) {
    return Py_BuildValue("d",  self->tol2D);
}

static PyObject *CoordSys_find2D(CoordSys *self, PyObject *args) {
    PyObject *PL=NULL;
    int norm=1, i, l;
    double u[3], v[3], w[3], p1[3], p2[3], d[3], tol;
    if (! PyArg_ParseTuple(args, "O|i", &PL, &norm))
	return CoordSys_Raise(ERR_ARG);
    if (! PySequence_Check(PL))
	return CoordSys_Raise(ERR_ARG);
    l = PySequence_Length(PL);
    tol = ((self->tol2D == DNDEF) ? 0.0 : self->tol2D);
    /* use first point as o */
    seq2vec(PySequence_GetItem(PL, 0), self->o);
    /* find p1, u */
    i = 0;
    do {
	if (++i >= l) return CoordSys_Raise(ERR_POL);
	vDiff(seq2vec(PySequence_GetItem(PL, i), p1), self->o, u);
    } while (vLen(u) <= tol);
    /* find third point p2 and w */
    do {
	if (++i >= l) return CoordSys_Raise(ERR_POL);
	vDiff(seq2vec(PySequence_GetItem(PL, i), p2), p1, d);
    } while ((vLen(d) <= tol) || (vLen(vCross(u, d, w)) <= tol));
    /* calculate v, make a rectangular system */
    vCross(w, u, v);
    if (norm) {
      vNorm(u); vNorm(v); vNorm(w);
    } else {
	/* use length of u for v and w */
	vMult(vNorm(v), vLen(u));
	vMult(vNorm(w), vLen(u));
    }
    if (PyErr_Occurred())
        return CoordSys_Raise(ERR_POL);
    self->m[0] = u[0]; self->m[1] = v[0]; self->m[2] = w[0];
    self->m[3] = u[1]; self->m[4] = v[1]; self->m[5] = w[1];
    self->m[6] = u[2]; self->m[7] = v[2]; self->m[8] = w[2];
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *CoordSys_getattr(CoordSys *self, char *name) {
    if (self->attr != NULL) {
	PyObject *v = PyDict_GetItemString(self->attr, name);
	if (v != NULL) {
	    Py_INCREF(v);
	    return v;
	}
    }
    return Py_FindMethod(CoordSys_Methods, (PyObject *)self, name);
}

static int CoordSys_setattr(CoordSys *self, char *name, PyObject *v) {
    if (self->attr == NULL) {
	self->attr = PyDict_New();
	if (self->attr == NULL)
	    return -1;
    }
    if (v == NULL) {
	int rv = PyDict_DelItemString(self->attr, name);
	if (rv < 0)
	    PyErr_SetString(PyExc_AttributeError,
			    "delete non-existing CoordSys attribute");
	return rv;
    }
    else
	return PyDict_SetItemString(self->attr, name, v);
}


static PyObject *CoordSys_repr(PyObject *self) {
    CoordSys *c = (CoordSys *)self;
    char buf[500];
    PyObject *s = PyString_FromString("<<CoordSys: [o] ||        [u] |        [v] |        [w]\n");
    sprintf(buf, "     %10g || %10g | %10g | %10g\n", c->o[0], c->m[0], c->m[1], c->m[2]);
    PyString_ConcatAndDel(&s, PyString_FromString(buf));
    sprintf(buf, "     %10g || %10g | %10g | %10g\n", c->o[1], c->m[3], c->m[4], c->m[5]);
    PyString_ConcatAndDel(&s, PyString_FromString(buf));
    sprintf(buf, "     %10g || %10g | %10g | %10g >>\n", c->o[2], c->m[6], c->m[7], c->m[8]);
    PyString_ConcatAndDel(&s, PyString_FromString(buf));
    Py_INCREF(s);
    return s;
}

static PyMethodDef CoordSys_Methods[] = {
  {"toGlobal",  (PyCFunction)CoordSys_toGlobal,    METH_O},
  {"toLocal",   (PyCFunction)CoordSys_toLocal,     METH_O},
  {"toLocal2D", (PyCFunction)CoordSys_toLocal2D,   METH_O},
  {"matrix",    (PyCFunction)CoordSys_matrix,      METH_NOARGS},
  {"offset",    (PyCFunction)CoordSys_offset,      METH_NOARGS},
  {"o",         (PyCFunction)CoordSys_offset,      METH_NOARGS},
  {"u",         (PyCFunction)CoordSys_u,           METH_NOARGS},
  {"v",         (PyCFunction)CoordSys_v,           METH_NOARGS},
  {"w",         (PyCFunction)CoordSys_w,           METH_NOARGS},
  {"setTol2D",  (PyCFunction)CoordSys_set2DTol,    METH_O},
  {"getTol2D",  (PyCFunction)CoordSys_get2DTol,    METH_NOARGS},
  {"find2D",    (PyCFunction)CoordSys_find2D,      METH_VARARGS},
  {NULL, NULL}, /* sentinel */
};

static PyTypeObject CoordSys_Type = {
  PyObject_HEAD_INIT(NULL)
  0,                               /*ob_size*/
  "CoordSys",                      /*tp_name*/
  sizeof(CoordSys),                /*tp_basicsize*/
  0,                               /*tp_itemsize*/
  /* methods */
  (destructor)CoordSys_dealloc,    /*tp_dealloc*/
  0,                               /*tp_print*/
  (getattrfunc)CoordSys_getattr,   /*tp_getattr*/
  (setattrfunc)CoordSys_setattr,   /*tp_setattr*/
  0,                               /*tp_compare*/
  (reprfunc)CoordSys_repr,         /* (reprfunc)tp_repr*/
  0,                               /*tp_as_number*/
  0,                               /*tp_as_sequence*/
  0,                               /*tp_as_mapping*/
  0,                               /*tp_hash*/
  0,                               /*tp_call*/
  0,                               /*tp_str*/
  0,                               /*tp_getattro*/
  0,                               /*tp_setattro*/
  0,                               /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT,              /*tp_flags*/
  0,                               /*tp_doc*/
  0,                               /*tp_traverse*/
  0,                               /*tp_clear*/
  0,                               /*tp_richcompare*/
  0,                               /*tp_weaklistoffset*/
  0,                               /*tp_iter*/
  0,                               /*tp_iternext*/
  0,                               /*tp_methods*/
  0,                               /*tp_members*/
  0,                               /*tp_getset*/
  0,                               /*tp_base*/
  0,                               /*tp_dict*/
  0,                               /*tp_descr_get*/
  0,                               /*tp_descr_set*/
  0,                               /*tp_dictoffset*/
  0,                               /*tp_init*/
  0,                               /*tp_alloc*/
  0,                               /*tp_new*/
  0,                               /*tp_free*/
  0,                               /*tp_is_gc*/
};


static PyMethodDef CoordSysMethods[] = {
    {"CoordSys",  CoordSys_new,  METH_VARARGS},
    {NULL, NULL}        /* Sentinel */
};

DL_EXPORT(void) initcCoordSys(void) {
    PyObject *m, *d;
    CoordSys_Type.ob_type = &PyType_Type;
    m = Py_InitModule("cCoordSys", CoordSysMethods);
    d = PyModule_GetDict(m);
    CoordSysError = PyErr_NewException("cCoordSys.Error", NULL, NULL);
    PyDict_SetItemString(d, "Error", CoordSysError);
    PyDict_SetItemString(d, "CoordSysType", (PyObject *)(&CoordSys_Type));
    PyDict_SetItemString(d, "version", (PyObject *)PyFloat_FromDouble(CSYSVERSION));
}
