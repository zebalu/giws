#!/usr/bin/python -u
from types import MethodType

class JNIFrameWork:
	"""
	This class provides the JNI code
	"""
	
	JavaVMVariable="jvm"
	JavaVMVariableType="JavaVM"
	
	def getHeader(self):
		return """#include <string>
		#include <iostream>
		#include <stdlib.h>
		#include <jni.h>
		"""

	def getJavaVMVariable(self):
		return self.JavaVMVariable
	
	def getJavaVMVariableType(self):
		return self.JavaVMVariableType

	def getMethodGetCurrentEnv(self,objectName):
		return """
		JNIEnv * %s::getCurrentEnv() {
		JNIEnv * curEnv = NULL;
		this->jvm->AttachCurrentThread((void **) &curEnv, NULL);
		return curEnv;
		}"""%(objectName)

	
	def getObjectDestuctor(self,objectName):
		return ("""
		%s::~%s() {
		JNIEnv * curEnv = NULL;
		this->jvm->AttachCurrentThread((void **) &curEnv, NULL);
		
		curEnv->DeleteGlobalRef(this->instance);
		curEnv->DeleteGlobalRef(this->instanceClass);
		}
		""")%(objectName, objectName)
	

	def getSynchronizeMethod(self,objectName):
		return ("""
		
		void %s::synchronize() {
		if (getCurrentEnv()->MonitorEnter(instance) != JNI_OK) {
		std::cerr << "Fail to enter monitor." << std::endl;
		exit(EXIT_FAILURE);
		}
		}
		""")%(objectName)
	
	def getEndSynchronizeMethod(self,objectName):
		return ("""
		void %s::endSynchronize() {
		if ( getCurrentEnv()->MonitorExit(instance) != JNI_OK) {
		std::cerr << "Fail to exit monitor." << std::endl;
		exit(EXIT_FAILURE);
		}
		}
		""")%(objectName)
	
	def getObjectInstanceProfile(self):		
		return """
		JNIEnv * curEnv = getCurrentEnv();
		""" 

	def getExceptionCheckProfile(self):
		return """
		if (curEnv->ExceptionOccurred()) {
		curEnv->ExceptionDescribe() ;
		}
		"""

	def getMethodIdProfile(self,method):
		params=""
		for parameter in method.getParameters():
			if parameter.getType().getIsArray(): # It is an array
				params+="["
			params+=parameter.getType().getTypeSignature()

		methodIdName=method.getUniqueNameOfTheMethod()
		
		signatureReturn=method.getReturn().getTypeSignature()
		if method.getReturn().getIsArray(): # Returns an array ... 
			signatureReturn="["+signatureReturn
		
		return ("""
		if (this->%s == NULL)
		{
		this->%s = curEnv->GetMethodID(this->instanceClass, "%s", "(%s)%s" ) ;
		if (this->%s == NULL) {
		std::cerr << "Could not access to the method %s" << std::endl;
		exit(EXIT_FAILURE);
		}
		}""")%(methodIdName, methodIdName, method.getName(), params,signatureReturn ,methodIdName, method.getName())

	def getCallObjectMethodProfile(self, method):
		parametersTypes=method.getParameters()
		returnType=method.getReturn()
		i=1
		params=""
		
		for parameter in parametersTypes:
			if i==1:
				params+="," # in order to manage call without param
			params+=parameter.getName()
			if hasattr(parameter.getType(), "specificPreProcessing") and type(parameter.getType().specificPreProcessing) is MethodType: 
				params+="_" # There is a pre-processing, then, we add the _ 
			if len(parametersTypes)!=i: 
				params+=", "
			i=i+1
			
		if returnType.getNativeType()=="void": # Dealing with a void ... 
			returns=""
		else:
			if returnType.getIsArray():
				typeOfReturn=returnType.getJavaTypeArraySyntax()
			else:
				typeOfReturn=returnType.getJavaTypeSyntax()
				
			returns="""%s res =  (%s)"""%(typeOfReturn, typeOfReturn)

		return """
	 	%s curEnv->%s( this->instance, %s %s);
		%s
""" % (returns, returnType.CallMethod(), method.getUniqueNameOfTheMethod(), params,self.getExceptionCheckProfile())

	def getReturnProfile(self, returnType):
		
		if hasattr(returnType, "specificReturn") and type(returnType.specificReturn) is MethodType: # When a specific kind of return is necessary (string for example)
			return returnType.specificReturn()
		else:
			return """
			return res;
			"""
		
