const app = (() => {
    return {
        init: () => {
            // fix Chart size hacker style = 500
            window.dispatchEvent(new Event('resize'));

            const element = {
                presentationSection: document.querySelector("#data-presentation-section"),
                presentationSectionLink: document.querySelector("#data-presentation"),
                analysisSection: document.querySelector("#data-analysis-section"),
                analysisSectionLink: document.querySelector("#data-analysis"),
                projectIntroSection: document.querySelector("#project-intro-section"),
                projectIntroSectionLink: document.querySelector("#project-intro"),
                tabs: document.querySelector(".tabs"),
                dataIntro1: document.querySelector(".dataIntro1"),
                collapsible: document.querySelector(".collapsible")
            }

            // initialize tabs
            M.AutoInit();

            const collapsibleInstance = M.Collapsible.init(element.collapsible, {onOpenStart: ()=>{window.dispatchEvent(new Event('resize'));}});
            // const tabsInstance = M.Tabs.init(element.tabs, {swipeable: false, onShow: ()=>{window.dispatchEvent(new Event('resize'));}});
            
            // tabsInstance.select('tab-monograms');
            // tabsInstance.updateTabIndicator();

            const createDataIntroAttribute = (hintText, element) => {
                element.setAttribute("data-intro", hintText)
            }

            const showAnalysisSection = () => {
                element.analysisSection.classList.remove("hide")
                element.presentationSection.classList.remove("hide")
                element.presentationSection.classList.add("hide")
                element.projectIntroSection.classList.remove("hide")
                element.projectIntroSection.classList.add("hide")
                // document.getElementsByClassName("background-image").style.backgroundImage="url('assets/img/accounting-close-up-computation-1418347.jpg')"
                document.body.style.backgroundImage="url('assets/img/accounting-close-up-computation-1418347.jpg')"
                document.body.style.background.filter="brightness(30%)";

            }

            const showPresentationSection = () => {
                element.presentationSection.classList.remove("hide")
                element.analysisSection.classList.remove("hide")
                element.analysisSection.classList.add("hide")
                element.projectIntroSection.classList.remove("hide")
                element.projectIntroSection.classList.add("hide")
                // document.getElementsByClassName("background-image").style.backgroundImage="url('assets/img/adult-connection-desk-374720.jpg')"
                document.body.style.backgroundImage="url('assets/img/adult-connection-desk-374720.jpg')"
                document.body.style.background.filter="brightness(30%)";
            }

            const showProjectIntroSection = () => {
                element.projectIntroSection.classList.remove("hide")
                element.analysisSection.classList.remove("hide")
                element.analysisSection.classList.add("hide")
                element.presentationSection.classList.remove("hide")
                element.presentationSection.classList.add("hide")
                // document.getElementsByClassName("background-image").style.backgroundImage="url('assets/img/charts-data-desk-669615.jpg')"
                document.body.style.backgroundImage="url('assets/img/charts-data-desk-669615.jpg')"
                document.body.style.background.filter="brightness(30%)";

                //initialization introJS
                if(!localStorage.getItem("wasProjectIntroSectionVisited")){
                    // creating dataIntro attributes
                    createDataIntroAttribute("dziaba",element.dataIntro1)

                    introJs().start();
                    localStorage.setItem("wasProjectIntroSectionVisited", true)
                }
            }

            element.analysisSectionLink.addEventListener("click", () => {
                showAnalysisSection()
            })

            element.presentationSectionLink.addEventListener("click", () => {
                showPresentationSection()
            })
        
            element.projectIntroSectionLink.addEventListener("click", () => {
                showProjectIntroSection()
            })
            
            showProjectIntroSection()
            console.log("initComplete")
        }
    }

})()

let time = setInterval(() => {
    let test = document.querySelector("#main-container")
    if (test) {
        app.init();
        clearInterval(time)
    }
}, 1000)




