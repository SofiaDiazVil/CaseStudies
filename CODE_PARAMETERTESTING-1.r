############ POWER ANALYSES ############
# loading packages
install.packages('pwr')
library(pwr)
library(ggplot2)


# hier benoem ik de  parameters voor de power analyse
effect.size <- 0.25  # 0.25 (small effect)
alpha <- 0.01       # alpha
sample <- 130        # sample size

# power test anova
pwr.anova.test(k = 2,         # k = 2 (2 groups: Japan vs. Scotland)
               n = sample,      
               f = effect.size,
               sig.level = alpha,
               power = NULL) #power = NULL because we have to measure this

############ COMFORMATORY ANALYSES ############
library(pacman)
pacman::p_load(dlookr, dplyr, foreign, ggcorrplot, ggthemes, hablar, lavaan, MBESS, naniar, pastecs, mice, lattice, reshape2, sos,
               readr, semTools, tidyverse,haven,ggplot2,plotly,tidyr,RPostgreSQL, RPostgres,insight, GGally, RColorBrewer,
               magrittr,jsonlite,purrr, stringr,anytime,lubridate, psych,e1071,lmerTest, afex, effectsize,car,sjstats, readxl)

library(dplyr)
library(summarytools)
data <- Parameters_lockdown
colnames(data)
group <- as.factor(data$Group)
drift <- as.numeric(data$Drift)
noise <- as.numeric(data$Noise)
boundry <- as.numeric(data$Boundry)
decision <- as.numeric(data$Decision)

### Discriptives ###
# voor elke variabele: gemiddelde en sd
## drift rate 
mean(drift[group == 'Japan'], na.rm = TRUE)
mean(drift[group == 'Scotland'], na.rm = TRUE)

# voor elke variabele: gemiddelde en sd
## depression 
sd(drift[group == 'Japan'], na.rm = TRUE)
sd(drift[group == 'Scotland'], na.rm = TRUE)

## noise
mean(decision[group == 'Japan'], na.rm = TRUE)
mean(decision[group == 'Scotland'], na.rm = TRUE)

# voor elke variabele: gemiddelde en sd
## depression 
sd(decision[group == 'Japan'], na.rm = TRUE)
sd(decision[group == 'Scotland'], na.rm = TRUE)


### Analyses ####
lm1 <- lm(drift + decision ~ group)
confint(lm1)
Anova(lm1, type="III")

res.man <- manova(cbind(drift, decision) ~ group, data = data)
summary(res.man)
summary.aov(res.man)

############ COMFORMATORY ANALYSES ############
## drift rate 
mean(noise[group == 'Japan'], na.rm = TRUE)
mean(noise[group == 'Scotland'], na.rm = TRUE)

# voor elke variabele: gemiddelde en sd
## depression 
sd(noise[group == 'Japan'], na.rm = TRUE)
sd(noise[group == 'Scotland'], na.rm = TRUE)

## noise
mean(boundry[group == 'Japan'], na.rm = TRUE)
mean(boundry[group == 'Scotland'], na.rm = TRUE)

# voor elke variabele: gemiddelde en sd
## depression 
sd(boundry[group == 'Japan'], na.rm = TRUE)
sd(boundry[group == 'Scotland'], na.rm = TRUE)

### Analyses ####
lm2 <- lm(drift + decision + noise + boundry ~ group)
confint(lm2)
Anova(lm2, type="III")

res.man <- manova(cbind(drift, decision, noise, boundry) ~ group, data = data)
summary(res.man)
summary.aov(res.man)

# boxplot 
# ddm
############ PLOTS ######################################################################################

#GGPLOT========================================================================================================================================
jitterSize= 1
Decisionplot<-ggplot(data=data,aes(x=group, y=decision,fill=group,colour=group,na.rm=TRUE)) +
  stat_summary(fun = "mean", geom = "bar",alpha=0.5)+
  stat_summary(fun.data = "mean_cl_boot", size=0.3,aes(colour = group))+ # 95 confidence interval
  geom_jitter(aes(y = decision,colour=group),alpha=0.3,width=0.05,height=0.1,size= jitterSize)+
  scale_y_continuous(limits=c(0,1),breaks = c(0, 0.5, 1)) +
  scale_x_discrete (name="Group",labels = c("Japan", "Scotland"))+
  labs(y = "Decision",x = "Group")+
  ggtitle("Decision")+
  scale_fill_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  scale_colour_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  theme_bw()

Decisionplot
#========================================================================================================================================
Driftplot<-ggplot(data=data,aes(x=group, y=drift,fill=group,colour=group,na.rm=TRUE)) +
  stat_summary(fun = "mean", geom = "bar",alpha=0.5)+
  stat_summary(fun.data = "mean_cl_boot", size=0.3,aes(colour = group))+ # 95 confidence interval
  geom_jitter(aes(y = drift,colour=group),alpha=0.3,width=0.05,height=0.1,size= jitterSize)+
  scale_y_continuous(limits=c(3,6),breaks = c(3, 4.5, 6)) +
  scale_x_discrete (name="Group",labels = c("Japan", "Scotland"))+
  labs(y = "Drift",x = "Group")+
  ggtitle("Drift")+
  scale_fill_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  scale_colour_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  theme_bw()

Driftplot

#========================================================================================================================================
boundryplot<-ggplot(data=data,aes(x=group, y= boundry,fill=group,colour=group,na.rm=TRUE)) +
  stat_summary(fun = "mean", geom = "bar",alpha=0.5)+
  stat_summary(fun.data = "mean_cl_boot", size=0.3,aes(colour = group))+ # 95 confidence interval
  geom_jitter(aes(y = boundry,colour=group),alpha=0.3,width=0.05,height=0.1,size= jitterSize)+
  scale_y_continuous(limits=c(0,1),breaks = c(0, 0.5, 1)) +
  scale_x_discrete (name="Group",labels = c("Japan", "Scotland"))+
  labs(y = "boundry",x = "Group")+
  ggtitle("boundry")+
  scale_fill_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  scale_colour_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  theme()

boundryplot

#========================================================================================================================================
Noiseplot<-ggplot(data=data,aes(x=group, y= noise,fill=group,colour=group,na.rm=TRUE)) +
  stat_summary(fun = "mean", geom = "bar",alpha=0.5)+
  stat_summary(fun.data = "mean_cl_boot", size=0.3,aes(colour = group))+ # 95 confidence interval
  geom_jitter(aes(y = noise,colour=group),alpha=0.3,width=0.05,height=0.1,size= jitterSize)+
  scale_y_continuous(limits=c(0,1),breaks = c(0, 0.5, 1)) +
  scale_x_discrete (name="Group",labels = c("Japan", "Scotland"))+
  labs(y = "noise",x = "Group")+
  ggtitle("noise")+
  scale_fill_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  scale_colour_manual(name="Group",labels=c("Japan","Scotland"),values=c("blue3","chartreuse4"))+
  theme()

Noiseplot

#========================================================================================================================================
install.packages("patchwork")
library(patchwork)
combinedpanel<-Noiseplot+ boundryplot+ Driftplot + Decisionplot+
  plot_annotation(tag_levels = 'A', title= "Factors")+
  plot_layout(guides = "collect",ncol = 2, widths = c(2, 2)) & theme(legend.position = "bottom")+
  theme(plot.tag = element_text(size = 12,face = 'bold'),
        plot.tag.position = "topleft")

combinedpanel
ggsave(combinedpanel, height=8 , width=8)

#BOXPLOT===================================================================================================================
plot(noise ~ group,
     data = data, 
     xlab = "group", 
     ylab = "Starting point(z)",
     col = "pink")

plot(drift ~ group,
     data = data, 
     xlab = "group", 
     ylab = "Drift Rate (v)",
     col = "pink")

plot(boundry ~ group,
     data = data, 
     xlab = "group", 
     ylab = "Treshold Separation (a)",
     col = "pink")

plot(decision ~ group,
     data = data, 
     xlab = "group", 
     ylab = "Non Decision Time (t0)",
     col = "pink")

# ddm via ppt

