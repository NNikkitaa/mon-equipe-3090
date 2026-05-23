
    try {
        app.project.items.addComp("Rendu_Cyber_3090", 1920, 1080); var layer = app.project.items.addSolid([0, 0, 0], "solide noir", 1920, 1080); app.project.items.addSolid([0, 255, 255], "solide cyan", 1920, 1080);
    } catch(e) {
        var file = new File("C:\\Users\\Hensen Martial\\Desktop\\mon_equipe_3090\\commande_agent.jsx.log");
        file.open("w");
        file.write(e.message + " à la ligne " + e.line);
        file.close();
    }
    