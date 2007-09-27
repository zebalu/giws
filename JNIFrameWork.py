#!/usr/bin/python -u
from types import MethodType

class JNIFrameWork:
	"""
	This class provides the JNI code
	"""
	
	JNIEnvVariable="JEnv"
	JNIEnvVariableType="JNIEnv"
	def getHeader(self):
		return """#include <string>
		#include <iostream>
		#include <stdlib.h>
		#include <jni.h>
		"""

	def JNIEnvAccess(self):
		return ("""%s->""" % self.JNIEnvVariable)

	def getJNIEnvVariable(self):
		return self.JNIEnvVariable
	
	def getJNIEnvVariableType(self):
		return self.JNIEnvVariableType
	
	def getObjectInstanceProfile(self):		
		return """
		jclass instanceClass = this->%sGetObjectClass(*instance);
		if (instanceClass == NULL) {
		std::cerr << "Could not get the Object Class " <<  std::endl;
		exit(EXIT_FAILURE);
		} 
		""" % self.JNIEnvAccess()

	def getMethodIdProfile(self, methodName, parametersTypes, returnType):
		params=""
		for parameter in parametersTypes:
			params+=parameter.getType().getTypeSignature()
		return ("""
		jmethodID methodId = this->%sGetMethodID(instanceClass, "%s", "(%s)%s" ) ;
		    if (methodId == NULL) {
			std::cerr << "Could not access to the method %s" << std::endl;
			exit(EXIT_FAILURE);
			}
		
		"""%(self.JNIEnvAccess(), methodName, params, returnType.getTypeSignature(),methodName))

	def getCallObjectMethodProfile(self,parametersTypes,returnType):
		i=1
		params=""
		for parameter in parametersTypes:
			if i==1:
				params+="," # in order to manage call without param
			params+=parameter.getName()
			if len(parametersTypes)!=i: 
				params+=", "
			i=i+1
		if returnType.getNativeType()=="void": # Dealing with a void ... 
			returns=""
		else:
			returns="""%s res ="""%returnType.getJavaTypeSyntax()

		return ("""
	 	%s (%s) this->%s%s( *this->instance, methodId %s);
""" % (returns, returnType.getJavaTypeSyntax(),  self.JNIEnvAccess(), returnType.CallMethod(), params ))

	def getReturnProfile(self, returnType):
		
		if hasattr(returnType, "specificReturn") and type(returnType.specificReturn) is MethodType: # When a specific kind of return is necessary (string for example)
			return returnType.specificReturn()
		else:
			return """
			return res;
			"""
		
