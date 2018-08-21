
package in.ac.iitb.cfilt.jhwnl.examples;
//package JHWNL;

//import py4j.GatewayServer;
import in.ac.iitb.cfilt.jhwnl.JHWNL;
import in.ac.iitb.cfilt.jhwnl.JHWNLException;
import in.ac.iitb.cfilt.jhwnl.data.IndexWord;
import in.ac.iitb.cfilt.jhwnl.data.IndexWordSet;
import in.ac.iitb.cfilt.jhwnl.data.Pointer;
import in.ac.iitb.cfilt.jhwnl.data.PointerType;
import in.ac.iitb.cfilt.jhwnl.data.Synset;
import in.ac.iitb.cfilt.jhwnl.data.POS;
import in.ac.iitb.cfilt.jhwnl.dictionary.Dictionary;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;

public class Synsets {
	private Synsets synsets;
	
	public static int getSenseCount(String word) {
		int size = 0;
		JHWNL.initialize();
		
		try {
			IndexWordSet demoIWSet = Dictionary.getInstance().lookupAllIndexWords(word.trim());				
			//	 Note: Use lookupAllMorphedIndexWords() to look up morphed form of the input word for all POS tags				
			IndexWord[] demoIndexWord = new IndexWord[demoIWSet.size()];
			demoIndexWord  = demoIWSet.getIndexWordArray();
			for ( int i = 0;i < demoIndexWord.length;i++ ) {
				size = demoIndexWord[i].getSenseCount();
				break;
			}
		}  catch (JHWNLException e) {
			System.err.println("Internal Error raised from API.");
			e.printStackTrace();
		}
		return size;
	}
	
	public static void main(String args[]) throws Exception {
		
	}
	
}
