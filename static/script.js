auth = () => {
    if (localStorage.getItem("username") == null) {
        redirect("/login")
    }
}

signout = () => {
    localStorage.clear()
    redirect("/login")
}

login = () => {
    localStorage.setItem("username", getInput("username"))
    localStorage.setItem("status", getInput("status"))
    localStorage.setItem("goal", getInput("goal"))
    localStorage.setItem("liked", "[]")
    redirect("/")
}

let netCals = 0
let netProt = 0

eat = (cals, prot) => {
    netCals += cals
    netProt += prot
}

calc = () => {
    let msg

    try {
        const inp = getInput("inp")

        if (localStorage.getItem("goal") == "Weight loss") {
            const diffCals = netCals - inp
            if ((diffCals < -500) & (diffCals >= -1000)) {
                msg = `You have burnt <span class="stallion">${-diffCals}</span> calories today. You're on track to lose a kilo this week!<h1 class="stallion">${diffCals}kCal</h1>`
            } else if ((diffCals < -0) & (diffCals >= -500)) {
                msg = `You have burnt <span class="stallion">${-diffCals}</span> calories today. You're on track to lose half a kilo this week!<h1 class="stallion">${diffCals}kCal</h1>`
            } else if (diffCals < -1000) {
                msg = `Whoa! Good going, but cool down! You burnt <span class="stallion">${-diffCals}</span> calories today.<h1 class="stallion">${diffCals}kCal</h1>`
            } else {
                msg = `Hmm... you could burn some more calories, because you gained <span class="stallion">${diffCals}</span> calories today. But, no worries: you got this!<h1 class="stallion">+${diffCals}kCal</h1>`
            }

        } else if (localStorage.getItem("goal") == "Muscle building") {
            const req = 1.5 * inp
            if (netProt > req) {
                msg = `Good going! You had <span class="stallion">${netProt.toFixed(1)}g</span> of protein today.<h1 class="stallion">${netProt.toFixed(1)}g</h1>`
            } else { msg = `Good try, but you need more protein. You only had <span class="stallion">${netProt.toFixed(1)}g</span> of protein today.<h1 class="stallion">${netProt.toFixed(1)}g</h1>` }
        }
    } catch {
        if (1 == 1) {
            msg = `Find your stats below.<p class="stallion">${netCals}kCal</p><p class="stallion">${netProt.toFixed(1)}g of protein</p>`
        }
    }

    setValue("msg", msg)
    document.getElementById("msg").style.display = "block"
    document.getElementById("msg").style.opacity = "1"
    document.getElementById("main").style.opacity = "0.25"
}

reportPopup = item => {
    setValue("msg", `<form method="POST" action="/report"><input type="hidden" name="item" value="${item}"><input type="email" class="form" name="email" placeholder="Email (purely optional)"> <button type="submit" class="btn btn-danger">&#9872 Report</button></form>`)
    document.getElementById("msg").style.display = "block"
    document.getElementById("msg").style.opacity = "1"
    document.getElementById("main").style.opacity = "0.25"
}

like = id => {
    let liked = eval(localStorage.getItem("liked"))
    liked.push(id)
    localStorage.setItem("liked", `[${liked.toString()}]`)
    redirect(`/post-${id}`)
}

checkLiked = id => {
    const liked = eval(localStorage.getItem("liked"))
    if (liked.includes(id)) {
        setValue("like", "You have liked this post.")
    }
}

optimizeFood = () => {
    if (localStorage.getItem("goal") == "Weight loss") {
        document.getElementById("weight").style.display = "table"
        document.getElementById("inp").placeholder = "How many calories did you burn today?"
    } else if (localStorage.getItem("goal") == "Muscle building") {
        document.getElementById("muscle").style.display = "table"
        document.getElementById("inp").placeholder = "What is your weight (in kilograms)?"
    } else {
        document.getElementById("overall").style.display = "table"
        setValue("form", "")
    }
}

optimizeFeed = () => {
    if (localStorage.getItem("goal") == "Weight loss") {
        document.getElementById("weight").style.display = "block"
    } else if (localStorage.getItem("goal") == "Muscle building") {
        document.getElementById("muscle").style.display = "block"
    } else {
        document.getElementById("overall").style.display = "block"
    }
}