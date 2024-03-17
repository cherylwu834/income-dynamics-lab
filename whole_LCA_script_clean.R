#main file for LCA classification for retail data from India, modified from section LCA file
#author: Cheryl Wu
#date: 08/28/2022-08/29/2022


#load in poLCA package
library(poLCA)


#read in data, data file is in same directory as working directory, read.table is a function in utils; T is effectively same as TRUE
processed_data <- read.table (file = "lca_processed.csv", header=T, as.is=T, sep=",")


#increases numbers in the data by one because they're supposed to be 1/2 not 0/1 for poLCA
for (i in 3:180){
  processed_data[,i] <- processed_data[i]+1
}


#check data looks correct
#print(head(processed_data, 5))
#print(dim(processed_data)) #should output 43447 rows 180 coloums


f1 <- as.formula(cbind(INDprod1,INDprod2,INDprod3,INDprod4,INDprod5,INDprod6,INDprod7,INDprod8,INDprod9,INDprod10,INDprod11,INDprod12,INDprod13,INDprod14,INDprod15,INDprod16,INDprod17,INDprod18,INDprod19,INDprod20,INDprod21,INDprod22,INDprod23,INDprod24,INDprod25,INDprod26,INDprod27,INDprod28,INDprod29,INDprod30,INDprod31,INDprod32,INDprod33,INDprod34,INDprod35,INDprod36,INDprod37,INDprod38,INDprod39,INDprod40,INDprod41,INDprod42,INDprod43,INDprod44,INDprod45,INDprod46,INDprod47,INDprod48,INDprod49,INDprod50,INDprod51,INDprod52,INDprod53,INDprod54,INDprod55,INDprod56,INDprod57,INDprod58,INDprod59,INDprod60,INDprod61,INDprod62,INDprod63,INDprod64,INDprod65,INDprod66,INDprod67,INDprod68,INDprod69,INDprod70,INDprod71,INDprod72,INDprod73,INDprod74,INDprod75,INDprod76,INDprod77,INDprod78,INDprod79,INDprod80,INDprod81,INDprod82,INDprod83,INDprod84,INDprod85,INDprod86,INDprod87,INDprod88,INDprod89,INDprod90,INDprod91,INDprod92,INDprod93,INDprod94,INDprod95,INDprod96,INDprod97,INDprod98,INDprod99,INDprod100,INDprod101,INDprod102,INDprod103,INDprod104,INDprod105,INDprod106,INDprod107,INDprod108,INDprod109,INDprod110,INDprod111,INDprod112,INDprod113,INDprod114,INDprod115,INDprod116,INDprod117,INDprod118,INDprod119,INDprod120,INDprod121,INDprod122,INDprod123,INDprod124,INDprod125,INDprod126,INDprod127,INDprod128,INDprod129,INDprod130,INDprod131,INDprod132,INDprod133,INDprod134,INDprod135,INDprod136,INDprod137,INDprod138,INDprod139,INDprod140,INDprod141,INDprod142,INDprod143,INDprod144,INDprod145,INDprod146,INDprod147,INDprod148,INDprod149,INDprod150,INDprod151,INDprod152,INDprod153,INDprod154,INDprod155,INDprod156,INDprod157,INDprod158,INDprod159,INDprod160,INDprod161,INDprod162,INDprod163,INDprod164,INDprod165,INDprod166,INDprod167,INDprod168,INDprod169,INDprod170,INDprod171,INDprod172,INDprod173,INDprod174,INDprod175,INDprod176,INDprod177,INDprod178)~1)


#runs a sequence of models with different number of classes and print out the model with the lowest BIC
min_bic <- 100000
for(i in 2:12) { #can change numbers in for loop to change range of number of classes
  lc <- poLCA(f1, data=processed_data, nclass=i, maxiter=5000, nrep=5, verbose=FALSE)
  print(paste(i, " classes, BIC is", lc$bic,",  time is", lc$time, ",  numiter is", lc$numiter ))
  if (lc$maxiter == lc$numiter){ 
    print("need to increase maxiter") #warn that maximum likelihood not found
  }
  if(lc$bic < min_bic){
    min_bic <- lc$bic
    LCA_best_model<-lc
  }
}  
LCA_best_model #shows results from LCA with lowest BIC value
