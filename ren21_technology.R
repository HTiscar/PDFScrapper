#install.packages("dplyr")
#install.packages("ggplot2")
#install.packages("gganimate")
#install.packages("gridExtra")
library(dplyr)
library(ggplot2)
library(gganimate)
library(gridExtra)

technology <- read.csv("ren21_technology.csv")
colnames(technology) <- c(seq(2008, 2018), "Sector")

tech <- as.data.frame(t(technology[1:11]))
tech$Years <- c(seq(2008, 2018))
tech$Years <- as.factor(tech$Years)
tech$Time <- seq_along(tech$Years)
colnames(tech) <- technology$Sector

### Revelar Plot Estático 

p <- ggplot(data = tech, aes(x = Years)) +
  geom_point(aes(y = Solarpower), color = "orange", size = 3) +
  geom_line(aes(y = Solarpower, group = 1, color = "orange"), size = 1) + 
  geom_point(aes(y = Windpower), color = "steelblue", size = 3) +
  geom_line(aes(y = Windpower, group = 1, color = "steelblue"), size = 1) +
  geom_point(aes(y = Biomass), color = "darkgreen", size = 3) +
  geom_line(aes(y = Biomass, group = 1, color = "darkgreen"), size = 1) +
  geom_point(aes(y = Biofuels), color = "green", size = 3) +
  geom_line(aes(y = Biofuels, group = 1, color = "green"), size = 1) +
  geom_point(aes(y = Geothermal), color = "brown", size = 3) +
  geom_line(aes(y = Geothermal, group = 1, color = "brown"), size = 1) + 
  geom_point(aes(y = Hydropower), color = "lightblue", size = 3) +
  geom_line(aes(y = Hydropower, group = 1, color = "lightblue"), size = 1) +
  geom_point(aes(y = Oceanpower), color = "navy", size = 3) +
  geom_line(aes(y = Oceanpower, group = 1, color = "navy"), size = 1) +
  xlab("Years") +
  ylab("Sector/Investment") +
  labs(title="Alternative Green Technology Investment",
       subtitle = "Billions USD",
       caption="Source: Ren21") + 
  scale_color_identity(name = "Sector",
                       breaks = c("orange", "steelblue", "darkgreen", "green", "brown", "lightblue", "navy"),
                       labels = c("Solar Power", "Wind Power", "Biomass", "Biofuels", "Geothermal", "Hydro Power", "Ocean Power"),
                       guide = "legend")

p

### Revelar Plot dynamico

q <- ggplot(data = tech, aes(x = Years)) +
  geom_point(aes(y = Solarpower), color = "orange", size = 3) +
  geom_line(aes(y = Solarpower, group = 1, color = "orange"), size = 1) + 
  geom_point(aes(y = Windpower), color = "steelblue", size = 3) +
  geom_line(aes(y = Windpower, group = 1, color = "steelblue"), size = 1) +
  geom_point(aes(y = Biomass), color = "darkgreen", size = 3) +
  geom_line(aes(y = Biomass, group = 1, color = "darkgreen"), size = 1) +
  geom_point(aes(y = Biofuels), color = "green", size = 3) +
  geom_line(aes(y = Biofuels, group = 1, color = "green"), size = 1) +
  geom_point(aes(y = Geothermal), color = "brown", size = 3) +
  geom_line(aes(y = Geothermal, group = 1, color = "brown"), size = 1) + 
  geom_point(aes(y = Hydropower), color = "lightblue", size = 3) +
  geom_line(aes(y = Hydropower, group = 1, color = "lightblue"), size = 1) +
  geom_point(aes(y = Oceanpower), color = "navy", size = 3) +
  geom_line(aes(y = Oceanpower, group = 1, color = "navy"), size = 1) +
  xlab("Years") +
  ylab("Sector/Investment") +
  labs(title="Alternative Green Technology Investment",
       subtitle = "Billions USD",
       caption="Source: Ren21") + 
  scale_color_identity(name = "Sector",
                       breaks = c("orange", "steelblue", "darkgreen", "green", "brown", "lightblue", "navy"),
                       labels = c("Solar Power", "Wind Power", "Biomass", "Biofuels", "Geothermal", "Hydro Power", "Ocean Power"),
                       guide = "legend") +
  transition_reveal(Time)

q

### Revelar Plot en forma de Grid 

p1 <- ggplot(data = tech, aes(x = Years)) +
  geom_point(aes(y = TotalNewInvestment), color = "red", size = 3) +
  geom_line(aes(y = TotalNewInvestment, group = 1), color = "red", size = 1) + 
  xlab("Years") +
  ylab("New Investment") +
  labs(title="Total New Investment", subtitle = "Billions USD", caption="Source: Ren21") 

p2 <- ggplot(data = tech, aes(x = Years)) +
  geom_point(aes(y = Solarpower), color = "orange", size = 3) +
  geom_line(aes(y = Solarpower, group = 1), color = "orange", size = 1) + 
  xlab("Years") +
  ylab("Solar Power/Investment") +
  labs(title="Solar Power Investment", caption="Source: Ren21") 

p3 <- ggplot(data = tech, aes(x = Years)) +
  geom_point(aes(y = Windpower), color = "steelblue", size = 3) +
  geom_line(aes(y = Windpower, group = 1), color = "steelblue", size = 1) + 
  xlab("Years") +
  ylab("Wind Power/Investment") +
  labs(title="Wind Power Investment", caption="Source: Ren21")

p4 <- ggplot(data = tech, aes(x = Years)) +
  geom_point(aes(y = Biomass), color = "darkgreen", size = 3) +
  geom_line(aes(y = Biomass, group = 1), color = "darkgreen", size = 1) + 
  xlab("Years") +
  ylab("Biomass/Investment") +
  labs(title="Biomass Investment", caption="Source: Ren21")


grid.arrange(p1,p2,p3,p4, layout_matrix = rbind(c(1,1,1),c(2,3,4))) 
