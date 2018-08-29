
package in.ac.iitb.cfilt.jhwnl.examples;

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

/*****************/
import java.io.*;
/*****************/
public class Examples {
	
	public static void demonstration() {
		
		BufferedReader inputWordsFile = null;
		try {
			/***********************************************/
		
        // Creating a File object that represents the disk file.
        PrintStream o = new PrintStream(new File("outtest.txt"), "utf-8");
 
        // Store current System.out before assigning a new value
        PrintStream console = System.out;
 
        // Assign o to output stream
        System.setOut(o);
		/***********************************************/
			inputWordsFile = new BufferedReader(new InputStreamReader (new FileInputStream ("inputwords.txt"), "UTF8"));
		} catch( FileNotFoundException e){
			System.err.println("Error opening input words file.");
			System.exit(-1);
		} catch (UnsupportedEncodingException e) {
			System.err.println("UTF-8 encoding is not supported.");
			System.exit(-1);
		}
		JHWNL.initialize();
		
		String inputLine;
		long[] synsetOffsets;
		
		
		try {
			while((inputLine = inputWordsFile.readLine()) != null){

				//System.out.println("\n" + inputLine);
				//	 Look up the word for all POS tags
				IndexWordSet demoIWSet = Dictionary.getInstance().lookupAllIndexWords(inputLine.trim());				
				//	 Note: Use lookupAllMorphedIndexWords() to look up morphed form of the input word for all POS tags				
				IndexWord[] demoIndexWord = new IndexWord[demoIWSet.size()];
				demoIndexWord  = demoIWSet.getIndexWordArray();
				for ( int i = 0;i < demoIndexWord.length;i++ ) {
					int size = demoIndexWord[i].getSenseCount();
					synsetOffsets = demoIndexWord[i].getSynsetOffsets();
					
					/***********************/
					ArrayList<ArrayList<String>> returnValue = new ArrayList();
					/***********************/
					Synset[] synsetArray = demoIndexWord[i].getSenses(); 
					for ( int k = 0;k < size;k++ ) {
						System.out.println("Synset [" + k +"] "+ synsetArray[k]);
						/***********************************************************/
						ArrayList<String> temp = new ArrayList();
						tempStr = synsetArray[k].substring(synsetArray[k].indexOf("[")+1, synsetArray[k].indexOf("]"));
						temp.add(tempStr.split(",").length);//synonyms
						temp.add(synsetArray[k].getPOS());
						tempHypernyms = "";
						tempHyponyms = "";
						Pointer[] pointers = synsetArray[k].getPointers();
						for (int j = 0; j < pointers.length; j++) {							
							if(!pointers[j].getType().equals(PointerType.ONTO_NODES)) {	// For ontology relation
								if(pointers[j].getType().equals("HYPERNYM")) {
									tempHypernyms += "," + pointers[j].getTargetSynset().substring(pointers[j].getTargetSynset().indexOf("[") + 1, pointers[j].getTargetSynset().indexOf("]"));
								} else if(pointers[j].getType().equals("HYPONYM")) {
									tempHypernyms = tempHypernyms.split(",");
									distinct = 0;
									 for(int i=0;i<tempHypernyms.length-1;i++){
										boolean isDistinct = false;
										for(int j=i+1;j<tempHypernyms.length;j++){
											if(arr[i] == arr[j]){
												isDistinct = true;
												break;
											}
										}
										if(!isDistinct){
											distinct++;
										}
									}
									temp.add(distinct);//no. of distinct hypernyms
									tempHyponyms += "," + pointers[j].getTargetSynset().substring(pointers[j].getTargetSynset().indexOf("[") + 1, pointers[j].getTargetSynset().indexOf("]"));
								} else if(pointers[j].getType().equals("ONTO_NODES")) {
									tempHyponyms = tempHyponyms.split(",");
									distinct = 0;
									 for(int i=0;i<tempHyponyms.length-1;i++){
										boolean isDistinct = false;
										for(int j=i+1;j<tempHyponyms.length;j++){
											if(arr[i] == arr[j]){
												isDistinct = true;
												break;
											}
										}
										if(!isDistinct){
											distinct++;
										}
									}
									temp.add(distinct);//no. of distinct hyponyms
								}
								
								System.out.println(pointers[j].getType() + " : "  + pointers[j].getTargetSynset());
							}							
						}
						returnValue.add(temp);
						return returnValue;
						/***********************************************************/
						System.out.println("Synset POS: " + synsetArray[k].getPOS());
						Pointer[] pointers = synsetArray[k].getPointers();
						System.out.println("Synset Num Pointers:" + pointers.length);
						for (int j = 0; j < pointers.length; j++) {							
							if(pointers[j].getType().equals(PointerType.ONTO_NODES)) {	// For ontology relation
								System.out.println(pointers[j].getType() + " : "  + Dictionary.getInstance().getOntoSynset(pointers[j].getOntoPointer()).getOntoNodes());
							} else {
								System.out.println(pointers[j].getType() + " : "  + pointers[j].getTargetSynset());
							}							
						}
						
					}
				}
				
			}
		} catch (IOException e) {
			System.err.println("Error in input/output.");			
			e.printStackTrace();
		} catch (JHWNLException e) {
			System.err.println("Internal Error raised from API.");
			e.printStackTrace();
		} 
	}
	
	public static void main(String args[]) throws Exception {
		demonstration();
	}
}
