dat <- read.csv('data.csv')
dat$percHoundwins <- dat$houndWins/(dat$houndWins + dat$hareWins)

gammas <- unique(dat$gamma)
cols <- c("red", "blue", "green", "orange", "purple", "pink", "black")
dat <- dat[with(dat, order(eta, gamma)), ]
for (r in unique(dat$runs)) {
  sdat <- dat[dat$runs == r, ] #subset(dat, dat$runs == r)
  plot(1, 0, xlim = c(0, 0.5), ylim = c(0, 1),
       main = paste("number of runs: ", r),
       xlab = "learning rate", ylab = "probability Hounds win")
  for (e in 1:length(cols)) {
    with(subset(sdat, sdat$gamma == gammas[e]),
         lines(eta, percHoundwins, col = cols[e]))
  }
  legend("bottomright", legend = gammas,
         col = cols, fill = cols, title = "gamma")
}

m <- with(dat, lm(percHoundwins ~ gamma + runs + eta))
summary(m)
