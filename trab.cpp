#include <SFML/Graphics.hpp>
#include <iostream>
#include <cstdlib>
#include <cmath>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Plano Cartesiano com Grid");
    window.setFramerateLimit(60);

    // Offset inicial do plano (centro dos eixos)
    sf::Vector2i offset(400, 300);

    // Controle do mouse
    bool dragging = false;
    sf::Vector2i prevMousePos;

    sf::Font font;
    if(!font.loadFromFile("/usr/share/fonts/truetype/dejavu/DejaVuMathTeXGyre.ttf"))
        std::cout << "Fonte não encontrada\n";
    std::vector<float> fatores = {1.0f, 2.0f, 5.0f};
    int gridSpacing = 50;
    double multiplicador = 1;
    int expoente = 0;
    int controle = 0;
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event)) 
        {
            if (event.type == sf::Event::Closed)
                window.close();

            // Começa o arrasto
            if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Left) {
                dragging = true;
                prevMousePos = sf::Mouse::getPosition(window);
            }

            // Termina o arrasto
            if (event.type == sf::Event::MouseButtonReleased && event.mouseButton.button == sf::Mouse::Left) {
                dragging = false;
            }

            // Arrastando
            if (event.type == sf::Event::MouseMoved && dragging) {
                sf::Vector2i mousePos = sf::Mouse::getPosition(window);
                sf::Vector2i delta = mousePos - prevMousePos;
                offset += delta;
                prevMousePos = mousePos;
            }
            
            if(event.type == sf::Event::MouseWheelMoved)
            {
                // std::cout << event.mouseWheel.delta << std::endl;
                gridSpacing += (event.mouseWheel.delta*5);
                
                if (gridSpacing < 50) {
                    gridSpacing = 100;
                
                    controle++;
                    if (controle >= fatores.size()) {
                        controle = 0;
                        expoente++;
                    }
                
                    multiplicador = fatores[controle] * std::pow(10, expoente);
                }
                
                if (gridSpacing > 100) {
                    gridSpacing = 50;
                
                    controle--;
                    if (controle < 0) {
                        controle = fatores.size() - 1;
                        expoente--;
                    }
                
                    multiplicador = fatores[controle] * std::pow(10, expoente);
                }           
            }
        }
    

        window.clear(sf::Color::White);

        // Desenhar grade vertical
        int x = offset.x%gridSpacing;
        if(x < 0)
        {
            x = x + 50;
        }

        int num_x = offset.y + 16;
        if(num_x < 16)
        {
            num_x = 16;
        }
        else
        {
            if(num_x > (window.getSize().y - 16))
            {
                num_x = window.getSize().y - 16;
            }
        }

        for (x; x < window.getSize().x; x += gridSpacing) 
        {
            sf::Vertex line[] = {
                sf::Vertex(sf::Vector2f(x, 0), sf::Color(220, 220, 220)),
                sf::Vertex(sf::Vector2f(x, window.getSize().y), sf::Color(220, 220, 220))
            };
            window.draw(line, 2, sf::Lines);

            sf::Text text;
            text.setFont(font);
            text.setString(std::to_string(((x - offset.x)/gridSpacing)*multiplicador));
            text.setCharacterSize(12);
            text.setFillColor(sf::Color::Black);
            sf::FloatRect bounds = text.getLocalBounds();
            text.setOrigin(bounds.left + bounds.width/2, bounds.top + bounds.height/2);
            text.setPosition(x, num_x);

            window.draw(text);
        }

        // Desenhar grade horizontal        
        int y = offset.y%gridSpacing;
        if(y < 0)
            y = y + 50;

        int num_y = offset.x - 10;
        if(num_y < 10)
        {
            num_y = 10;
        }
        else
        {
            if(num_y > (window.getSize().x - 10))
            {
                num_y = window.getSize().x - 10;
            }
        }

        for (y; y < window.getSize().y; y += gridSpacing) {
            sf::Vertex line[] = {
                sf::Vertex(sf::Vector2f(0, y), sf::Color(220, 220, 220)),
                sf::Vertex(sf::Vector2f(window.getSize().x, y), sf::Color(220, 220, 220))
            };
            window.draw(line, 2, sf::Lines);
            sf::Text text;
            text.setFont(font);
            text.setString(std::to_string(((offset.y - y)/gridSpacing)*multiplicador));
            text.setCharacterSize(12);
            text.setFillColor(sf::Color::Black);
            sf::FloatRect bounds = text.getLocalBounds();
            text.setOrigin(bounds.left + bounds.width, bounds.top + bounds.height/2);
            int teste = num_y;
            if(num_y - bounds.width < 10)
            {
                text.setOrigin(bounds.left, bounds.top + bounds.height/2);
                teste = 10;
                // teste = num_y + bounds.width;
            }
            text.setPosition(teste, y);

            window.draw(text);
        }

        // Desenhar eixo Y
        if (offset.x >= 0 && offset.x <= window.getSize().x) {
            sf::Vertex yAxis[] = {
                sf::Vertex(sf::Vector2f(offset.x, 0), sf::Color::Black),
                sf::Vertex(sf::Vector2f(offset.x, window.getSize().y), sf::Color::Black)
            };
            window.draw(yAxis, 2, sf::Lines);
        }

        // Desenhar eixo X
        if (offset.y >= 0 && offset.y <= window.getSize().y) {
            sf::Vertex xAxis[] = {
                sf::Vertex(sf::Vector2f(0, offset.y), sf::Color::Black),
                sf::Vertex(sf::Vector2f(window.getSize().x, offset.y), sf::Color::Black)
            };
            window.draw(xAxis, 2, sf::Lines);
        }

        window.display();
    }

    return 0;
}

