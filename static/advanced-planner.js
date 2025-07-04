/* Kitchen Planner Pro - JavaScript Avancé */

class KitchenPlannerPro {
    constructor() {
        this.selectedElement = null;
        this.currentTool = 'select';
        this.isDragging = false;
        this.isResizing = false;
        this.showDimensions = false;
        this.placedEquipment = [];
        this.chefs = [];
        this.dragOffset = { x: 0, y: 0 };
        this.snapToGrid = true;
        this.gridSize = 20;
        this.history = [];
        this.historyIndex = -1;
        this.magneticSnap = true;
        this.collisionDetection = true;
        
        this.init();
    }
    
    init() {
        this.initializeDragAndDrop();
        this.initializeCanvas();
        this.initializeKeyboardShortcuts();
        this.initializeContextMenu();
        this.initializeMagneticSnap();
        this.updateStats();
        this.loadFromStorage();
    }
    
    // Initialisation du canvas
    initializeCanvas() {
        const canvas = document.getElementById('canvas');
        const kitchenLayout = document.getElementById('kitchen-layout');
        
        if (!canvas || !kitchenLayout) {
            console.error('Elements canvas non trouvés');
            return;
        }
        
        // Gestion des clics sur le canvas
        canvas.addEventListener('click', (e) => {
            if (e.target === canvas || e.target.id === 'kitchen-layout') {
                this.deselectAll();
            }
        });
        
        // Prévenir le scroll avec la molette
        canvas.addEventListener('wheel', (e) => {
            if (e.ctrlKey) {
                e.preventDefault();
                // Zoom futur
            }
        });
        
        console.log('✅ Canvas initialisé');
    }
    
    // Drag & Drop avancé avec magnétisme
    initializeDragAndDrop() {
        const equipmentItems = document.querySelectorAll('.equipment-item');
        const canvas = document.getElementById('kitchen-layout');
        
        equipmentItems.forEach(item => {
            item.addEventListener('dragstart', (e) => this.handleDragStart(e, item));
            item.addEventListener('dragend', (e) => this.handleDragEnd(e, item));
        });
        
        canvas.addEventListener('dragover', (e) => this.handleDragOver(e));
        canvas.addEventListener('drop', (e) => this.handleDrop(e));
        canvas.addEventListener('dragenter', (e) => this.handleDragEnter(e));
        canvas.addEventListener('dragleave', (e) => this.handleDragLeave(e));
    }
    
    handleDragStart(e, item) {
        const data = {
            type: item.dataset.type,
            width: parseInt(item.dataset.width),
            height: parseInt(item.dataset.height),
            name: item.textContent.trim()
        };
        
        e.dataTransfer.setData('text/plain', JSON.stringify(data));
        item.classList.add('dragging');
        
        // Créer une image de prévisualisation
        const dragImage = this.createDragPreview(data);
        e.dataTransfer.setDragImage(dragImage, data.width / 2, data.height / 2);
        
        // Montrer les zones de drop
        this.showDropZones();
    }
    
    handleDragEnd(e, item) {
        item.classList.remove('dragging');
        this.hideDropZones();
    }
    
    handleDragOver(e) {
        e.preventDefault();
        
        // Magnétisme en temps réel
        if (this.magneticSnap) {
            const rect = document.getElementById('kitchen-layout').getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const snappedPos = this.snapToGrid({ x, y });
            this.updateDropPreview(snappedPos);
        }
    }
    
    handleDrop(e) {
        e.preventDefault();
        const data = JSON.parse(e.dataTransfer.getData('text/plain'));
        const rect = document.getElementById('kitchen-layout').getBoundingClientRect();
        
        let x = e.clientX - rect.left;
        let y = e.clientY - rect.top;
        
        // Appliquer le magnétisme
        if (this.snapToGrid) {
            const snapped = this.snapToGrid({ x, y });
            x = snapped.x;
            y = snapped.y;
        }
        
        // Vérifier les collisions
        if (this.collisionDetection && this.checkCollision(x, y, data.width, data.height)) {
            this.showTooltip('Collision détectée ! Positionnement automatique...', e.clientX, e.clientY);
            const newPos = this.findSafePosition(data.width, data.height);
            x = newPos.x;
            y = newPos.y;
        }
        
        this.createEquipment(data, x, y);
        this.saveState();
    }
    
    // Magnétisme et grille
    snapToGrid(pos) {
        return {
            x: Math.round(pos.x / this.gridSize) * this.gridSize,
            y: Math.round(pos.y / this.gridSize) * this.gridSize
        };
    }
    
    initializeMagneticSnap() {
        // Attirer les éléments vers les guides et autres équipements
        document.addEventListener('mousemove', (e) => {
            if (!this.isDragging || !this.magneticSnap) return;
            
            const magneticFields = this.detectMagneticFields();
            const elementRect = this.selectedElement.getBoundingClientRect();
            const canvasRect = document.getElementById('kitchen-layout').getBoundingClientRect();
            
            let bestSnap = null;
            let minDistance = 30; // Distance magnétique
            
            magneticFields.forEach(field => {
                const distance = this.calculateDistance(
                    { x: elementRect.left - canvasRect.left, y: elementRect.top - canvasRect.top },
                    field.position
                );
                
                if (distance < minDistance) {
                    minDistance = distance;
                    bestSnap = field;
                }
            });
            
            if (bestSnap) {
                this.showMagneticGuide(bestSnap);
            }
        });
    }
    
    detectMagneticFields() {
        const fields = [];
        
        // Bords d'autres équipements
        this.placedEquipment.forEach(eq => {
            const rect = eq.getBoundingClientRect();
            const canvasRect = document.getElementById('kitchen-layout').getBoundingClientRect();
            
            fields.push({
                type: 'equipment-edge',
                position: {
                    x: rect.left - canvasRect.left,
                    y: rect.top - canvasRect.top
                },
                strength: 20
            });
        });
        
        // Murs et guides
        fields.push(
            { type: 'wall', position: { x: 50, y: 0 }, strength: 25 },
            { type: 'wall', position: { x: 0, y: 50 }, strength: 25 }
        );
        
        return fields;
    }
    
    // Détection de collision avancée
    checkCollision(x, y, width, height) {
        const newRect = { x, y, width, height };
        
        return this.placedEquipment.some(eq => {
            const existingRect = {
                x: parseInt(eq.style.left),
                y: parseInt(eq.style.top),
                width: parseInt(eq.style.width),
                height: parseInt(eq.style.height)
            };
            
            return this.rectanglesOverlap(newRect, existingRect);
        });
    }
    
    rectanglesOverlap(rect1, rect2) {
        return !(rect1.x + rect1.width <= rect2.x ||
                rect2.x + rect2.width <= rect1.x ||
                rect1.y + rect1.height <= rect2.y ||
                rect2.y + rect2.height <= rect1.y);
    }
    
    findSafePosition(width, height) {
        const canvas = document.getElementById('kitchen-layout');
        const canvasWidth = canvas.offsetWidth;
        const canvasHeight = canvas.offsetHeight;
        
        // Recherche en spirale
        for (let radius = 0; radius < 500; radius += this.gridSize) {
            for (let angle = 0; angle < 360; angle += 45) {
                const x = 200 + radius * Math.cos(angle * Math.PI / 180);
                const y = 200 + radius * Math.sin(angle * Math.PI / 180);
                
                if (x >= 0 && y >= 0 && 
                    x + width <= canvasWidth && 
                    y + height <= canvasHeight &&
                    !this.checkCollision(x, y, width, height)) {
                    return this.snapToGrid({ x, y });
                }
            }
        }
        
        return { x: 100, y: 100 }; // Position par défaut
    }
    
    // Création d'équipement avec animations
    createEquipment(data, x, y) {
        const equipment = document.createElement('div');
        equipment.className = 'placed-equipment equipment-enter';
        equipment.style.left = x + 'px';
        equipment.style.top = y + 'px';
        equipment.style.width = data.width + 'px';
        equipment.style.height = data.height + 'px';
        equipment.textContent = data.name;
        equipment.dataset.type = data.type;
        equipment.dataset.category = this.getEquipmentCategory(data.type);
        equipment.dataset.id = 'eq_' + Date.now();
        
        // Ajouter les handles de redimensionnement
        this.addResizeHandles(equipment);
        
        // Ajouter les event listeners
        equipment.addEventListener('mousedown', (e) => this.startDrag(e, equipment));
        equipment.addEventListener('click', (e) => this.selectEquipment(e, equipment));
        equipment.addEventListener('contextmenu', (e) => this.showContextMenu(e, equipment));
        
        // Animation d'entrée
        setTimeout(() => equipment.classList.remove('equipment-enter'), 600);
        
        document.getElementById('kitchen-layout').appendChild(equipment);
        this.placedEquipment.push(equipment);
        
        this.updateStats();
        this.createDimensions(equipment);
        this.validateHACCP();
    }
    
    getEquipmentCategory(type) {
        const categories = {
            'four': 'cuisson',
            'plancha': 'cuisson', 
            'friteuse': 'cuisson',
            'grill': 'cuisson',
            'frigo': 'refrigeration',
            'congelateur': 'refrigeration',
            'cellule': 'refrigeration',
            'table': 'preparation',
            'billot': 'preparation',
            'plan': 'preparation',
            'etagere': 'stockage'
        };
        return categories[type] || 'general';
    }
    
    addResizeHandles(equipment) {
        // Ajouter des poignées de redimensionnement
        const positions = ['nw', 'ne', 'sw', 'se'];
        positions.forEach(pos => {
            const handle = document.createElement('div');
            handle.className = `resize-handle ${pos}`;
            handle.dataset.position = pos;
            equipment.appendChild(handle);
        });
    }
    
    getEquipmentCategory(type) {
        const categories = {
            'four': 'cuisson',
            'plancha': 'cuisson',
            'friteuse': 'cuisson',
            'grill': 'cuisson',
            'frigo': 'refrigeration',
            'congelateur': 'refrigeration',
            'cellule': 'refrigeration',
            'cave': 'refrigeration',
            'plonge': 'lavage',
            'lave-vaisselle': 'lavage',
            'evier': 'lavage',
            'bac': 'lavage',
            'table': 'preparation',
            'billot': 'preparation',
            'plan': 'preparation',
            'etagere': 'preparation'
        };
        return categories[type] || 'other';
    }
    
    // Validation HACCP en temps réel
    validateHACCP() {
        this.clearHACCPWarnings();
        
        const violations = this.checkHACCPCompliance();
        violations.forEach(violation => this.showHACCPWarning(violation));
        
        this.updateEfficiencyScore();
    }
    
    checkHACCPCompliance() {
        const violations = [];
        
        // Vérifier séparation cuisson/froid
        const cooking = this.placedEquipment.filter(eq => eq.dataset.category === 'cuisson');
        const cold = this.placedEquipment.filter(eq => eq.dataset.category === 'refrigeration');
        
        cooking.forEach(cookEq => {
            cold.forEach(coldEq => {
                const distance = this.calculateEquipmentDistance(cookEq, coldEq);
                if (distance < 100) { // 1 mètre minimum
                    violations.push({
                        type: 'thermal_separation',
                        elements: [cookEq, coldEq],
                        message: `Distance insuffisante: ${distance.toFixed(0)}cm`
                    });
                }
            });
        });
        
        // Vérifier largeur des couloirs
        const corridorViolations = this.checkCorridorWidths();
        violations.push(...corridorViolations);
        
        return violations;
    }
    
    showHACCPWarning(violation) {
        violation.elements.forEach(element => {
            element.classList.add('collision-warning');
            this.showTooltip(violation.message, 
                parseInt(element.style.left) + parseInt(element.style.width) / 2,
                parseInt(element.style.top) - 10
            );
        });
    }
    
    clearHACCPWarnings() {
        document.querySelectorAll('.collision-warning').forEach(el => {
            el.classList.remove('collision-warning');
        });
    }
    
    // Système de tooltips
    showTooltip(message, x, y) {
        let tooltip = document.getElementById('dynamic-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'dynamic-tooltip';
            tooltip.className = 'tooltip';
            document.body.appendChild(tooltip);
        }
        
        tooltip.textContent = message;
        tooltip.style.left = x + 'px';
        tooltip.style.top = (y - 40) + 'px';
        tooltip.classList.add('visible');
        
        setTimeout(() => {
            tooltip.classList.remove('visible');
        }, 3000);
    }
    
    // Raccourcis clavier
    initializeKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'z':
                        e.preventDefault();
                        this.undo();
                        break;
                    case 'y':
                        e.preventDefault();
                        this.redo();
                        break;
                    case 's':
                        e.preventDefault();
                        this.saveLayout();
                        break;
                    case 'a':
                        e.preventDefault();
                        this.selectAll();
                        break;
                    case 'd':
                        e.preventDefault();
                        this.duplicateSelected();
                        break;
                }
            } else {
                switch(e.key) {
                    case 'Delete':
                    case 'Backspace':
                        this.deleteSelected();
                        break;
                    case 'Escape':
                        this.deselectAll();
                        break;
                    case 'g':
                        this.toggleGrid();
                        break;
                    case 'm':
                        this.toggleMagneticSnap();
                        break;
                    case 'd':
                        this.toggleDimensions();
                        break;
                }
            }
        });
    }
    
    // Menu contextuel
    initializeContextMenu() {
        document.addEventListener('contextmenu', (e) => {
            if (e.target.classList.contains('placed-equipment')) {
                e.preventDefault();
                this.showContextMenu(e, e.target);
            }
        });
    }
    
    showContextMenu(e, element) {
        let menu = document.getElementById('context-menu');
        if (!menu) {
            menu = this.createContextMenu();
        }
        
        menu.style.left = e.clientX + 'px';
        menu.style.top = e.clientY + 'px';
        menu.classList.add('visible');
        menu.dataset.targetId = element.dataset.id;
        
        // Fermer au clic ailleurs
        setTimeout(() => {
            document.addEventListener('click', () => {
                menu.classList.remove('visible');
            }, { once: true });
        }, 100);
    }
    
    createContextMenu() {
        const menu = document.createElement('div');
        menu.id = 'context-menu';
        menu.className = 'context-menu';
        menu.innerHTML = `
            <div class="context-item" onclick="planner.duplicateElement()">🔄 Dupliquer</div>
            <div class="context-item" onclick="planner.rotateElement()">🔄 Rotation</div>
            <div class="context-item" onclick="planner.editProperties()">⚙️ Propriétés</div>
            <div class="context-item" onclick="planner.bringToFront()">⬆️ Premier plan</div>
            <div class="context-item" onclick="planner.sendToBack()">⬇️ Arrière-plan</div>
            <div class="context-item danger" onclick="planner.deleteElement()">🗑️ Supprimer</div>
        `;
        document.body.appendChild(menu);
        return menu;
    }
    
    // Animations des cuisiniers
    addChef() {
        const chef = document.createElement('div');
        chef.className = 'chef';
        chef.innerHTML = '👨‍🍳';
        chef.style.left = (200 + Math.random() * 300) + 'px';
        chef.style.top = (150 + Math.random() * 200) + 'px';
        chef.dataset.id = 'chef_' + Date.now();
        chef.dataset.mood = 'happy';
        chef.dataset.task = 'idle';
        
        // Faire marcher le cuisinier
        chef.addEventListener('mousedown', (e) => this.startDrag(e, chef));
        chef.addEventListener('dblclick', () => this.animateChef(chef));
        
        document.getElementById('kitchen-layout').appendChild(chef);
        this.chefs.push(chef);
        this.updateStats();
        
        // Animation d'entrée
        chef.style.transform = 'scale(0)';
        setTimeout(() => {
            chef.style.transform = 'scale(1)';
            chef.style.transition = 'transform 0.3s ease';
        }, 100);
        
        // Démarrer l'animation de marche aléatoire
        this.startChefWalking(chef);
    }
    
    animateChef(chef) {
        chef.classList.add('chef-walking');
        setTimeout(() => chef.classList.remove('chef-walking'), 4000);
    }
    
    startChefWalking(chef) {
        const walkInterval = setInterval(() => {
            if (!document.body.contains(chef)) {
                clearInterval(walkInterval);
                return;
            }
            
            // Mouvement aléatoire
            const currentX = parseInt(chef.style.left);
            const currentY = parseInt(chef.style.top);
            const maxMove = 30;
            
            const newX = Math.max(50, Math.min(600, currentX + (Math.random() - 0.5) * maxMove));
            const newY = Math.max(50, Math.min(400, currentY + (Math.random() - 0.5) * maxMove));
            
            chef.style.left = newX + 'px';
            chef.style.top = newY + 'px';
            
            // Changer d'humeur occasionnellement
            if (Math.random() < 0.1) {
                const moods = ['😊', '😎', '🤔', '😅', '🙂'];
                chef.innerHTML = moods[Math.floor(Math.random() * moods.length)];
            }
            
        }, 3000 + Math.random() * 5000); // Toutes les 3-8 secondes
    }
    
    // Sauvegarde et historique
    saveState() {
        const state = {
            equipment: this.placedEquipment.map(eq => this.serializeEquipment(eq)),
            chefs: this.chefs.map(chef => this.serializeChef(chef)),
            timestamp: Date.now()
        };
        
        // Ajouter à l'historique
        this.history = this.history.slice(0, this.historyIndex + 1);
        this.history.push(state);
        this.historyIndex++;
        
        // Limiter la taille de l'historique
        if (this.history.length > 50) {
            this.history.shift();
            this.historyIndex--;
        }
        
        // Sauvegarder dans localStorage
        localStorage.setItem('kitchenPlannerState', JSON.stringify(state));
    }
    
    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.loadState(this.history[this.historyIndex]);
        }
    }
    
    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.loadState(this.history[this.historyIndex]);
        }
    }
    
    loadState(state) {
        // Effacer le canvas
        this.clearAll(false);
        
        // Restaurer les équipements
        state.equipment.forEach(data => {
            this.createEquipment(data, data.x, data.y);
        });
        
        // Restaurer les cuisiniers
        state.chefs.forEach(data => {
            this.addChef();
            const chef = this.chefs[this.chefs.length - 1];
            chef.style.left = data.x + 'px';
            chef.style.top = data.y + 'px';
        });
    }
    
    // Utilitaires
    calculateDistance(point1, point2) {
        return Math.sqrt(Math.pow(point1.x - point2.x, 2) + Math.pow(point1.y - point2.y, 2));
    }
    
    calculateEquipmentDistance(eq1, eq2) {
        const center1 = {
            x: parseInt(eq1.style.left) + parseInt(eq1.style.width) / 2,
            y: parseInt(eq1.style.top) + parseInt(eq1.style.height) / 2
        };
        const center2 = {
            x: parseInt(eq2.style.left) + parseInt(eq2.style.width) / 2,
            y: parseInt(eq2.style.top) + parseInt(eq2.style.height) / 2
        };
        
        return this.calculateDistance(center1, center2);
    }
    
    serializeEquipment(eq) {
        return {
            type: eq.dataset.type,
            name: eq.textContent,
            x: parseInt(eq.style.left),
            y: parseInt(eq.style.top),
            width: parseInt(eq.style.width),
            height: parseInt(eq.style.height),
            category: eq.dataset.category
        };
    }
    
    serializeChef(chef) {
        return {
            x: parseInt(chef.style.left),
            y: parseInt(chef.style.top),
            mood: chef.dataset.mood,
            task: chef.dataset.task
        };
    }
    
    loadFromStorage() {
        const saved = localStorage.getItem('kitchenPlannerState');
        if (saved) {
            try {
                const state = JSON.parse(saved);
                this.loadState(state);
            } catch (e) {
                console.warn('Erreur lors du chargement de la sauvegarde:', e);
            }
        }
    }
    
    // Interface publique
    toggleGrid() {
        this.snapToGrid = !this.snapToGrid;
        const canvas = document.getElementById('canvas');
        canvas.classList.toggle('magnetic-grid', this.snapToGrid);
    }
    
    toggleMagneticSnap() {
        this.magneticSnap = !this.magneticSnap;
    }
    
    updateStats() {
        let totalSurface = 0;
        this.placedEquipment.forEach(eq => {
            const width = parseInt(eq.style.width) / 100;
            const height = parseInt(eq.style.height) / 100;
            totalSurface += width * height;
        });
        
        document.getElementById('total-surface').textContent = totalSurface.toFixed(1) + ' m²';
        document.getElementById('equipment-count').textContent = this.placedEquipment.length;
        document.getElementById('chef-count').textContent = this.chefs.length;
        
        const efficiency = this.calculateEfficiency();
        document.getElementById('efficiency').textContent = efficiency + '%';
    }
    
    calculateEfficiency() {
        // Calcul d'efficacité plus sophistiqué
        let score = 100;
        
        // Pénalités pour violations HACCP
        const violations = this.checkHACCPCompliance();
        score -= violations.length * 10;
        
        // Bonus pour organisation
        const categories = {};
        this.placedEquipment.forEach(eq => {
            const cat = eq.dataset.category;
            if (!categories[cat]) categories[cat] = [];
            categories[cat].push(eq);
        });
        
        // Bonus si les équipements de même catégorie sont groupés
        Object.values(categories).forEach(group => {
            if (group.length > 1) {
                const avgDistance = this.calculateGroupCompactness(group);
                if (avgDistance < 200) score += 5; // Bonus pour groupement
            }
        });
        
        return Math.max(50, Math.min(100, Math.round(score)));
    }
    
    calculateGroupCompactness(equipmentGroup) {
        let totalDistance = 0;
        let count = 0;
        
        for (let i = 0; i < equipmentGroup.length; i++) {
            for (let j = i + 1; j < equipmentGroup.length; j++) {
                totalDistance += this.calculateEquipmentDistance(equipmentGroup[i], equipmentGroup[j]);
                count++;
            }
        }
        
        return count > 0 ? totalDistance / count : 0;
    }
    
    // Méthodes manquantes essentielles
    deselectAll() {
        document.querySelectorAll('.placed-equipment, .chef').forEach(el => {
            el.classList.remove('selected');
        });
        this.selectedElement = null;
    }
    
    showDropZones() {
        const canvas = document.getElementById('kitchen-layout');
        canvas.classList.add('drop-zone-active');
    }
    
    hideDropZones() {
        const canvas = document.getElementById('kitchen-layout');
        canvas.classList.remove('drop-zone-active');
    }
    
    selectTool(tool) {
        this.currentTool = tool;
        document.querySelectorAll('.tool-btn').forEach(btn => btn.classList.remove('active'));
        const activeBtn = document.querySelector(`[onclick*="${tool}"]`);
        if (activeBtn) activeBtn.classList.add('active');
        
        console.log(`🛠️ Outil sélectionné: ${tool}`);
    }
    
    deleteSelected() {
        if (this.selectedElement) {
            this.selectedElement.remove();
            this.placedEquipment = this.placedEquipment.filter(eq => eq !== this.selectedElement);
            this.chefs = this.chefs.filter(chef => chef !== this.selectedElement);
            this.selectedElement = null;
            this.updateStats();
            this.saveState();
        }
    }
    
    clearAll(saveHistory = true) {
        this.placedEquipment.forEach(eq => eq.remove());
        this.chefs.forEach(chef => chef.remove());
        this.placedEquipment = [];
        this.chefs = [];
        this.selectedElement = null;
        this.updateStats();
        if (saveHistory) this.saveState();
    }
    
    saveLayout() {
        const state = {
            equipment: this.placedEquipment.map(eq => this.serializeEquipment(eq)),
            chefs: this.chefs.map(chef => this.serializeChef(chef)),
            timestamp: Date.now()
        };
        localStorage.setItem('kitchenPlannerState', JSON.stringify(state));
        console.log('💾 Layout sauvegardé');
    }
    
    exportLayout() {
        const layout = this.getCurrentLayout();
        const blob = new Blob([JSON.stringify(layout, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kitchen-layout-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
        console.log('📁 Layout exporté');
    }
    
    getCurrentLayout() {
        return {
            equipment: this.placedEquipment.map(eq => this.serializeEquipment(eq)),
            chefs: this.chefs.map(chef => this.serializeChef(chef)),
            stats: {
                totalSurface: document.getElementById('total-surface')?.textContent || '0 m²',
                equipmentCount: this.placedEquipment.length,
                chefCount: this.chefs.length,
                efficiency: document.getElementById('efficiency')?.textContent || '100%'
            },
            timestamp: new Date().toISOString()
        };
    }
    
    toggleDimensions() {
        this.showDimensions = !this.showDimensions;
        if (this.showDimensions) {
            this.placedEquipment.forEach(eq => this.createDimensions(eq));
        } else {
            document.querySelectorAll('.dimension-line, .dimension-label').forEach(el => el.remove());
        }
        console.log(`📏 Cotations ${this.showDimensions ? 'activées' : 'désactivées'}`);
    }
    
    createDimensions(element) {
        if (!this.showDimensions) return;
        
        // Supprimer anciennes dimensions
        if (element.dimensionElements) {
            element.dimensionElements.forEach(el => el.remove());
        }
        
        const left = parseInt(element.style.left);
        const top = parseInt(element.style.top);
        const width = parseInt(element.style.width);
        const height = parseInt(element.style.height);
        
        // Créer les lignes de cotation
        const widthLine = document.createElement('div');
        widthLine.className = 'dimension-line dimension-horizontal';
        widthLine.style.left = left + 'px';
        widthLine.style.top = (top - 15) + 'px';
        widthLine.style.width = width + 'px';
        
        const widthLabel = document.createElement('div');
        widthLabel.className = 'dimension-label';
        widthLabel.textContent = width + ' cm';
        widthLabel.style.left = (left + width/2 - 20) + 'px';
        widthLabel.style.top = (top - 25) + 'px';
        
        const heightLine = document.createElement('div');
        heightLine.className = 'dimension-line dimension-vertical';
        heightLine.style.left = (left - 15) + 'px';
        heightLine.style.top = top + 'px';
        heightLine.style.height = height + 'px';
        
        const heightLabel = document.createElement('div');
        heightLabel.className = 'dimension-label';
        heightLabel.textContent = height + ' cm';
        heightLabel.style.left = (left - 45) + 'px';
        heightLabel.style.top = (top + height/2 - 10) + 'px';
        
        const layout = document.getElementById('kitchen-layout');
        layout.appendChild(widthLine);
        layout.appendChild(widthLabel);
        layout.appendChild(heightLine);
        layout.appendChild(heightLabel);
        
        element.dimensionElements = [widthLine, widthLabel, heightLine, heightLabel];
    }
    
    // Méthodes HACCP manquantes
    checkCorridorWidths() {
        // Implémentation basique de vérification des couloirs
        const violations = [];
        // Pour l'instant, on considère que les couloirs sont conformes
        return violations;
    }
    
    updateEfficiencyScore() {
        const score = this.calculateEfficiency();
        const efficiencyEl = document.getElementById('efficiency');
        if (efficiencyEl) {
            efficiencyEl.textContent = score + '%';
        }
    }
    
    showTooltip(message, x, y) {
        // Créer ou réutiliser le tooltip
        let tooltip = document.getElementById('haccp-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'haccp-tooltip';
            tooltip.style.cssText = `
                position: absolute;
                background: #dc2626;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            `;
            document.body.appendChild(tooltip);
        }
        
        tooltip.textContent = message;
        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
        tooltip.style.display = 'block';
        
        // Auto-hide après 3 secondes
        setTimeout(() => {
            tooltip.style.display = 'none';
        }, 3000);
    }
    
    // Méthodes d'interaction manquantes
    startDrag(e, element) {
        if (this.currentTool === 'delete') {
            this.deleteElement(element);
            return;
        }
        
        if (this.currentTool !== 'select' && this.currentTool !== 'move') return;
        
        e.preventDefault();
        this.selectedElement = element;
        this.isDragging = true;
        
        const rect = element.getBoundingClientRect();
        const canvasRect = document.getElementById('kitchen-layout').getBoundingClientRect();
        
        const offsetX = e.clientX - rect.left;
        const offsetY = e.clientY - rect.top;
        
        const drag = (e) => {
            if (!this.isDragging) return;
            
            const x = e.clientX - canvasRect.left - offsetX;
            const y = e.clientY - canvasRect.top - offsetY;
            
            element.style.left = Math.max(0, x) + 'px';
            element.style.top = Math.max(0, y) + 'px';
            
            this.createDimensions(element);
        };
        
        const stopDrag = () => {
            this.isDragging = false;
            document.removeEventListener('mousemove', drag);
            document.removeEventListener('mouseup', stopDrag);
            this.saveState();
        };
        
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', stopDrag);
    }
    
    selectEquipment(e, equipment) {
        e.stopPropagation();
        
        // Désélectionner tous
        this.deselectAll();
        
        // Sélectionner actuel
        equipment.classList.add('selected');
        this.selectedElement = equipment;
        
        console.log(`Sélectionné: ${equipment.textContent}`);
    }
    
    deleteElement(element) {
        if (element.dimensionElements) {
            element.dimensionElements.forEach(el => el.remove());
        }
        
        this.placedEquipment = this.placedEquipment.filter(eq => eq !== element);
        this.chefs = this.chefs.filter(chef => chef !== element);
        
        element.remove();
        this.selectedElement = null;
        
        this.updateStats();
        this.saveState();
        console.log('Élément supprimé !');
    }
    
    // Méthodes drag & drop manquantes
    createDragPreview(data) {
        const preview = document.createElement('div');
        preview.style.cssText = `
            width: ${data.width}px;
            height: ${data.height}px;
            background: rgba(59, 130, 246, 0.3);
            border: 2px solid #3b82f6;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: #1e40af;
        `;
        preview.textContent = data.name;
        return preview;
    }
    
    updateDropPreview(position) {
        // Mise à jour visuelle de la zone de drop
        let preview = document.getElementById('drop-preview');
        if (!preview) {
            preview = document.createElement('div');
            preview.id = 'drop-preview';
            preview.style.cssText = `
                position: absolute;
                border: 2px dashed #10b981;
                background: rgba(16, 185, 129, 0.1);
                pointer-events: none;
                z-index: 5;
                border-radius: 6px;
            `;
            document.getElementById('kitchen-layout').appendChild(preview);
        }
        
        preview.style.left = position.x + 'px';
        preview.style.top = position.y + 'px';
        preview.style.display = 'block';
    }
    
    hideDropPreview() {
        const preview = document.getElementById('drop-preview');
        if (preview) {
            preview.style.display = 'none';
        }
    }
    
    handleDragEnter(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
    }
    
    handleDragLeave(e) {
        e.preventDefault();
        this.hideDropPreview();
    }
    
    // Configuration depuis le configurateur
    applyKitchenConfig(config) {
        if (!config || !config.dimensions) return;
        
        console.log('🏗️ Application de la configuration:', config);
        
        // Mettre à jour les dimensions du canvas
        const canvas = document.getElementById('kitchen-layout');
        if (canvas) {
            const scale = 100; // 1m = 100px
            const newWidth = config.dimensions.length * scale;
            const newHeight = config.dimensions.width * scale;
            
            canvas.style.minWidth = newWidth + 'px';
            canvas.style.minHeight = newHeight + 'px';
            
            // Effacer le canvas actuel
            canvas.innerHTML = '';
            
            // Redessiner avec la nouvelle configuration
            this.drawKitchenStructure(config, scale);
        }
        
        // Mettre à jour le titre
        const logo = document.querySelector('.logo span');
        if (logo) {
            logo.textContent = config.name || 'Kitchen Planner Pro';
        }
        
        // Afficher les dimensions dans les stats
        const surface = config.dimensions.length * config.dimensions.width;
        document.getElementById('total-surface').textContent = surface.toFixed(1) + ' m²';
        
        console.log(`✅ Configuration appliquée: ${config.dimensions.length}m × ${config.dimensions.width}m`);
    }
    
    drawKitchenStructure(config, scale) {
        const canvas = document.getElementById('kitchen-layout');
        const { length, width } = config.dimensions;
        
        // Dessiner les murs extérieurs
        this.drawWalls(canvas, length * scale, width * scale);
        
        // Dessiner les murs intérieurs si définis
        if (config.structure && config.structure.walls) {
            config.structure.walls.forEach(wall => {
                this.drawCustomWall(canvas, wall, scale);
            });
        }
        
        // Dessiner les portes si définies
        if (config.structure && config.structure.doors) {
            config.structure.doors.forEach(door => {
                this.drawCustomDoor(canvas, door, scale);
            });
        }
        
        // Dessiner les fenêtres si définies
        if (config.structure && config.structure.windows) {
            config.structure.windows.forEach(window => {
                this.drawCustomWindow(canvas, window, scale);
            });
        }
    }
    
    drawWalls(canvas, width, height) {
        const wallThickness = 20;
        
        // Mur du haut
        const topWall = document.createElement('div');
        topWall.className = 'wall horizontal';
        topWall.style.cssText = `
            position: absolute;
            top: 20px;
            left: 20px;
            width: ${width}px;
            height: ${wallThickness}px;
            background: #374151;
            z-index: 1;
        `;
        canvas.appendChild(topWall);
        
        // Mur du bas
        const bottomWall = document.createElement('div');
        bottomWall.className = 'wall horizontal';
        bottomWall.style.cssText = `
            position: absolute;
            top: ${height + 20 - wallThickness}px;
            left: 20px;
            width: ${width}px;
            height: ${wallThickness}px;
            background: #374151;
            z-index: 1;
        `;
        canvas.appendChild(bottomWall);
        
        // Mur de gauche
        const leftWall = document.createElement('div');
        leftWall.className = 'wall vertical';
        leftWall.style.cssText = `
            position: absolute;
            top: 20px;
            left: 20px;
            width: ${wallThickness}px;
            height: ${height}px;
            background: #374151;
            z-index: 1;
        `;
        canvas.appendChild(leftWall);
        
        // Mur de droite
        const rightWall = document.createElement('div');
        rightWall.className = 'wall vertical';
        rightWall.style.cssText = `
            position: absolute;
            top: 20px;
            left: ${width + 20 - wallThickness}px;
            width: ${wallThickness}px;
            height: ${height}px;
            background: #374151;
            z-index: 1;
        `;
        canvas.appendChild(rightWall);
    }
    
    drawCustomWall(canvas, wall, scale) {
        const wallElement = document.createElement('div');
        wallElement.className = 'wall';
        wallElement.style.cssText = `
            position: absolute;
            left: ${wall.x}px;
            top: ${wall.y}px;
            width: ${wall.width}px;
            height: ${wall.height}px;
            background: #374151;
            z-index: 1;
        `;
        canvas.appendChild(wallElement);
    }
    
    drawCustomDoor(canvas, door, scale) {
        const doorElement = document.createElement('div');
        doorElement.className = 'door';
        doorElement.style.cssText = `
            position: absolute;
            left: ${door.x}px;
            top: ${door.y}px;
            width: ${door.width}px;
            height: ${door.height}px;
            background: #059669;
            border: 2px solid #047857;
            border-radius: 3px;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        `;
        doorElement.textContent = '🚪';
        canvas.appendChild(doorElement);
    }
    
    drawCustomWindow(canvas, window, scale) {
        const windowElement = document.createElement('div');
        windowElement.className = 'window';
        windowElement.style.cssText = `
            position: absolute;
            left: ${window.x}px;
            top: ${window.y}px;
            width: ${window.width}px;
            height: ${window.height}px;
            background: #0ea5e9;
            border: 2px solid #0284c7;
            border-radius: 3px;
            z-index: 2;
        `;
        canvas.appendChild(windowElement);
    }
}

// Instance globale
let planner;

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    planner = new KitchenPlannerPro();
    
    // Fonctions globales pour les boutons
    window.addChef = () => planner.addChef();
    window.toggleDimensions = () => planner.toggleDimensions();
    window.saveLayout = () => planner.saveLayout();
    window.exportLayout = () => planner.exportLayout();
    window.clearAll = () => planner.clearAll();
    window.selectTool = (tool) => planner.selectTool(tool);
    window.deleteSelected = () => planner.deleteSelected();
});
