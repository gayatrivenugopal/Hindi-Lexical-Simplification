
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
import java.util.ArrayList;
/*****************/
public class Properties {
	
	public static ArrayList<ArrayList<String>> getProperties(String word) {
		
		BufferedReader inputWordsFile = null;
		try {
			/***********************************************/
		
        // Creating a File object that represents the disk file.
        //PrintStream o = new PrintStream(new File("outtest.txt"), "utf-8");
 
        // Store current System.out before assigning a new value
        //PrintStream console = System.out;
 
        // Assign o to output stream
        //System.setOut(o);
		/***********************************************/
		
		JHWNL.initialize();
		
		long[] synsetOffsets;
		
		
			
				//System.out.println("\n" + inputLine);
				//	 Look up the word for all POS tags
				IndexWordSet demoIWSet = Dictionary.getInstance().lookupAllIndexWords(word.trim());				
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
						String tempStr = synsetArray[k].toString().substring(synsetArray[k].toString().indexOf("[")+1, synsetArray[k].toString().indexOf("]"));
						temp.add(Integer.toString(tempStr.split(",").length));//synonyms
						System.out.println("temp: "+ temp.toString());
						temp.add(synsetArray[k].getPOS().toString());//POS
						System.out.println("temp: "+ temp.toString());
						String tempHypernyms = "";
						String tempHyponyms = "";
						Pointer[] pointers = synsetArray[k].getPointers();
						String previous = "";
						for (int j = 0; j < pointers.length; j++) {
							if(pointers[j].getType().equals(PointerType.ONTO_NODES)) {	// For ontology relation
								System.out.println(pointers[j].getType() + " : "  + Dictionary.getInstance().getOntoSynset(pointers[j].getOntoPointer()).getOntoNodes());
							} else {
								System.out.println(pointers[j].getType() + " : "  + pointers[j].getTargetSynset());
							}	
							
							
							//if(!pointers[j].getType().equals(PointerType.ONTO_NODES)) {	// For ontology relation
							//System.out.print(pointers[j].getType() + " " + pointers[j].getTargetSynset().toString().substring(pointers[j].getTargetSynset().toString().indexOf("[") + 1, pointers[j].getTargetSynset().toString().indexOf("]")));
								if(pointers[j].getType().toString().equals("HYPERNYM")) {
									tempHypernyms += "," + pointers[j].getTargetSynset().toString().substring(pointers[j].getTargetSynset().toString().indexOf("[") + 1, pointers[j].getTargetSynset().toString().indexOf("]"));
									System.out.print("tempHypernyms: " + tempHypernyms);
									previous = "hypernym";
								} else if(pointers[j].getType().toString().equals("HYPONYM") && previous!="hyponym") {
									String[] tempHypernymsArray = tempHypernyms.split(",");
									System.out.print("Array: ");
									for(int p=0; p<tempHypernymsArray.length; p++) {
										System.out.print(tempHypernymsArray[p] + " ");
									}
									int distinct = 0;
									int lastElementFlag = 0;
									 for(int index=1;index<tempHypernymsArray.length-1;index++){
										boolean isDistinct = true;
										for(int counter=index+1;counter<tempHypernymsArray.length;counter++){
											if(tempHypernymsArray[index] == tempHypernymsArray[counter]){
												isDistinct = false;
												if(counter == tempHypernymsArray.length -1)
													lastElementFlag = 1;
												break;
											}
										}
										if(isDistinct){
											distinct++;
										}
									}
									if(lastElementFlag == 0) {
										distinct++;
									}
									temp.add(Integer.toString(distinct));//no. of distinct hypernyms
									System.out.println("temp: "+ temp.toString());
									tempHyponyms += "," + pointers[j].getTargetSynset().toString().substring(pointers[j].getTargetSynset().toString().indexOf("[") + 1, pointers[j].getTargetSynset().toString().indexOf("]"));
									System.out.print("tempHyponyms: " + tempHyponyms);
									previous = "hyponym";
								} else if(pointers[j].getType().toString().equals("HYPONYM") && previous=="hyponym") {
									String[] tempHyponymsArray = tempHyponyms.split(",");
									int distinct = 0;
									int lastElementFlag = 0;
									 for(int index=1;index<tempHyponymsArray.length-1;index++){
										boolean isDistinct = false;
										for(int counter=index+1;counter<tempHyponymsArray.length;counter++){
											if(tempHyponymsArray[index] == tempHyponymsArray[counter]){
												isDistinct = true;
												if(counter == tempHyponymsArray.length -1)
													lastElementFlag = 1;
												break;
											}
										}
										if(!isDistinct){
											distinct++;
										}
									}
									if(lastElementFlag == 0) {
										distinct++;
									}
									temp.add(Integer.toString(distinct));//no. of distinct hyponyms
									System.out.print("temp: "+ temp.toString());
									tempHyponyms += "," + pointers[j].getTargetSynset().toString().substring(pointers[j].getTargetSynset().toString().indexOf("[") + 1, pointers[j].getTargetSynset().toString().indexOf("]"));
									System.out.print("tempHyponyms: " + tempHyponyms);
									previous = "hyponym";
								} else if(pointers[j].getType().toString().equals("ONTO_NODES")) {
									System.out.print("ONTO NODES");
									String[] tempHyponymsArray = tempHyponyms.split(",");
									int distinct = 0;
									int lastElementFlag = 0;
									 for(int index=1;index<tempHyponymsArray.length-1;index++){
										boolean isDistinct = false;
										for(int counter=index+1;counter<tempHyponymsArray.length;counter++){
											if(tempHyponymsArray[index] == tempHyponymsArray[counter]){
												isDistinct = true;
												if(counter == tempHyponymsArray.length -1)
													lastElementFlag = 1;
												break;
											}
										}
										if(!isDistinct){
											distinct++;
										}
									}
									if(lastElementFlag == 0) {
										distinct++;
									}
									temp.add(Integer.toString(distinct));//no. of distinct hyponyms
									System.out.print("temp: "+ temp.toString());
								}
								
								//System.out.println(pointers[j].getType() + " : "  + pointers[j].getTargetSynset());
							//}		
								returnValue.add(temp);							
						}
						
						System.out.println("Synset POS: " + synsetArray[k].getPOS());
						System.out.println("Synset Num Pointers:" + pointers.length);
						
						/***********************************************************/
						/*
						System.out.println("Synset POS: " + synsetArray[k].getPOS());
						pointers = synsetArray[k].getPointers();
						System.out.println("Synset Num Pointers:" + pointers.length);
						for (int j = 0; j < pointers.length; j++) {							
							if(pointers[j].getType().equals(PointerType.ONTO_NODES)) {	// For ontology relation
								System.out.println(pointers[j].getType() + " : "  + Dictionary.getInstance().getOntoSynset(pointers[j].getOntoPointer()).getOntoNodes());
							} else {
								System.out.println(pointers[j].getType() + " : "  + pointers[j].getTargetSynset());
							}							
						}*/
						
						
					}
					return returnValue;
				}
		} catch (JHWNLException e) {
			System.err.println("Internal Error raised from API.");
			e.printStackTrace();
		} 
		/*************/
		return null;
		/*************/
	}
	
	public static void main(String args[]) throws Exception {
		//demonstration();
	}
}
