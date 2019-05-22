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
                tabs: document.querySelector(".tabs"),
            }
            // initialize tabs
            M.AutoInit();
            
            const tabsInstance = M.Tabs.init(element.tabs, {swipeable: false, onShow: ()=>{window.dispatchEvent(new Event('resize'));}});
            tabsInstance.select('tab-monograms');
            tabsInstance.updateTabIndicator();


            const showAnalysisSection = () => {
                element.analysisSection.classList.remove("hide")
                element.presentationSection.classList.remove("hide")
                element.presentationSection.classList.add("hide")
            }

            const showPresentationSection = () => {
                element.presentationSection.classList.remove("hide")
                element.analysisSection.classList.remove("hide")
                element.analysisSection.classList.add("hide")
            }

            element.analysisSectionLink.addEventListener("click", () => {
                showAnalysisSection()
            })

            element.presentationSectionLink.addEventListener("click", () => {
                showPresentationSection()
            })
            showPresentationSection();
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




