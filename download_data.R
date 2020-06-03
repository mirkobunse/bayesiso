library("OpenML")

setOMLConfig(server="http://www.openml.org/api/v1", apikey="yourkey")

datasets = listOMLDataSets(limit=NULL)
temp <- datasets[datasets$number.of.classes == 2 & datasets$number.of.features >= 2 &
           datasets$number.of.features <= 300 & datasets$number.of.instances >= 20000 &
             datasets$number.of.instances <= 1000000 & datasets$number.of.missing.values == 0 &
             datasets$number.of.symbolic.features == 1, c("name", "data.id", "number.of.classes",
                                                         "number.of.instances",
                                                         "number.of.features",
                                                         "number.of.numeric.features",
                                                         "majority.class.size", "status")]
temp <- temp[!is.na(temp$data.id),]
temp$majority.class.percentage = temp$majority.class.size / temp$number.of.instances

# temp$name <- paste(temp$name,c(1:length(temp$name)), sep="_")
dim(temp)
head(temp)

names <- c(
  "SEA(50)",
  "BNG(breast-w)",
  "BNG(sonar)",
  "BNG(heart-statlog)",
  "creditcard",
  "numerai28.6",
  "2dplanes",
  "house_16H",
  "cal_housing",
  "houses",
  "house_8L",
  "fried",
  "letter",
  "BNG(spectf_test)",
  "BNG(Australian)",
  "BNG(SPECTF)",
  "Click_prediction_small",
  "Click_prediction_small",
  "Click_prediction_small",
  "skin-segmentation"
)

print("STARTING")
for (i in seq_along(names)) {
  name <- names[i]
  did <- temp[temp$name == name,]$data.id
  if (is.element(name, names)) {
    path <- paste("data/csvs/", name, "_", i, ".csv", sep="")
    if (!file.exists(path)) {
      result = tryCatch({
        data = getOMLDataSet(data.id = did)
        cat("READ FROM CACHE:", name, "\n")
        write.table(data$data, path)
        cat("WRITTEN:", path, "\n")
      }, warning = function(w) {
        cat("WARNING: ")
        print(w)
      }, error = function(e) {
        cat("ERROR: ")
        print(e)
      })
    } else {
      cat("FOUND:", path, "\n")
    }
  }
}
